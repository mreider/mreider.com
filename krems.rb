require 'sinatra'
require 'fileutils'
require 'redcarpet'
require 'pathname'
require 'toml-rb'
require 'date'

# Directories
MARKDOWN_DIR = "markdown"
CSS_DIR = "css"
IMAGES_DIR = "images"

# Default content for generated index.md
DEFAULT_INDEX_CONTENT = <<~MARKDOWN
  +++
  title = "Welcome to Krems"
  author = "Krems"
  date = "#{Time.now.strftime('%Y-%m-%d')}"
  summary = "Krems is running, but there was no index.md page, so I generated this one instead 😊."
  +++

  # Welcome to Krems

  Krems is running, but there was no `index.md` page, so I generated this one instead. 😊
MARKDOWN

# Create a default index.md if it doesn't exist
def ensure_index_md
  index_file = File.join(MARKDOWN_DIR, "index.md")
  unless File.exist?(index_file)
    FileUtils.mkdir_p(MARKDOWN_DIR)
    File.write(index_file, DEFAULT_INDEX_CONTENT)
  end
end

# Load defaults from defaults.toml if it exists
def load_defaults
  defaults_file = "defaults.toml"
  File.exist?(defaults_file) ? TomlRB.load_file(defaults_file) : {}
end

# Merge defaults into front matter
def merge_defaults(front_matter, defaults)
  defaults.each do |key, value|
    front_matter[key] = value unless front_matter.key?(key)
  end
  front_matter
end

# Parse optional front matter and apply defaults
def parse_front_matter(content, defaults)
  if content.strip.start_with?("+++")
    front_matter, body = content.split("+++", 3)[1..2]
    merged_front_matter = merge_defaults(TomlRB.parse(front_matter), defaults)
    [merged_front_matter, body.strip]
  else
    [defaults, content.strip]
  end
end

# Converts Markdown links from `.md` to `.html`
def convert_links_to_html(content, _current_folder = "")
  content.gsub(/href="(\/?[a-zA-Z0-9\-_\/\.]+)\.md"/) do
    link = $1
    # Force absolute paths
    absolute_path = link.start_with?("/") ? link : "/#{link}"
    "href=\"#{absolute_path}.html\""
  end
end

# Converts Markdown image links to absolute references
def update_image_links(content)
  content.gsub(/!\[([^\]]*)\]\((\/images\/[^\)]+)\)/) do
    alt_text, image_path = $1, $2
    "![#{alt_text}](#{image_path})"
  end
end

# Generates Open Graph meta tags from front matter
def generate_meta_tags(front_matter)
  tags = []
  tags << "<meta property=\"og:title\" content=\"#{front_matter['title']}\" />" if front_matter['title']
  tags << "<meta property=\"og:author\" content=\"#{front_matter['author']}\" />" if front_matter['author']
  tags << "<meta property=\"og:description\" content=\"#{front_matter['summary']}\" />" if front_matter['summary']
  tags << "<meta property=\"og:image\" content=\"/#{front_matter['image']}\" />" if front_matter['image']
  tags << "<meta property=\"og:date\" content=\"#{front_matter['date']}\" />" if front_matter['date']
  tags.join("\n")
end

# Generates an unstyled menu from front matter
def generate_menu(front_matter)
  return "" unless front_matter["menu"]

  menu_items = front_matter["menu"].map do |entry|
    formatted_path = entry["path"].gsub(/^\//, "").sub(/\.md$/, ".html")
    display_name = entry["name"].gsub(/([a-z])([A-Z])/, '\1 \2') # PascalCase formatting
    "<td><h4><a href=\"/#{formatted_path}\">#{display_name}</a></h4></td>"
  end

  menu_with_bullets = menu_items.join('<td><h4>•</h4></td>')
  "<table><tr>#{menu_with_bullets}</tr></table>"
end

# Generates static asset links in the <head> section
def generate_static_asset_links
  <<~HTML
    <link rel="stylesheet" href="/css/styles.css">
    <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/images/favicon-16x16.png">
    <link rel="manifest" href="/images/site.webmanifest">
    <link rel="icon" href="/images/favicon.ico">
    <meta name="theme-color" content="#ffffff">
  HTML
end

# Generates a list of posts in the specified folder
def generate_post_list(folder_name)
  folder_path = File.join(MARKDOWN_DIR, folder_name)
  return "" unless Dir.exist?(folder_path)

  posts_by_year = Dir.glob(File.join(folder_path, "*.md")).each_with_object(Hash.new { |h, k| h[k] = [] }) do |file, years|
    content = File.read(file)
    front_matter, _ = parse_front_matter(content, {})
    next unless front_matter["date"]

    year = Date.parse(front_matter["date"]).year
    display_name = File.basename(file, ".md").tr("_-", " ").capitalize
    link_path = "/#{folder_name}/#{File.basename(file, '.md')}.html" # Force absolute paths
    years[year] << { name: display_name, link: link_path }
  end

  sorted_years = posts_by_year.keys.sort.reverse
  sorted_years.map do |year|
    <<~HTML
      <h4>#{year}</h4>
      <ul>
        #{posts_by_year[year].sort_by { |post| post[:name] }.map { |post| "<li><a href=\"#{post[:link]}\">#{post[:name]}</a></li>" }.join("\n")}
      </ul>
    HTML
  end.join("\n")
end

# Replaces custom handlebars in content
def replace_custom_handlebars(content)
  content.gsub(/\{\{\s*list_posts\(([^)]+)\)\s*\}\}/) do
    folder_name = $1.strip
    generate_post_list(folder_name)
  end
end

# Hardcoded footer
def generate_footer
  <<~HTML
    <footer>
      <h4>&copy; 2024-2025 Matt Reider &bull; site generated with <a href="https://github.com/mreider/krems">krems</a></h4>
    </footer>
    </body>
    </html>
  HTML
end

# Processes Markdown files to HTML
def convert_markdown_to_html
  # Load defaults
  defaults = load_defaults

  # Initialize Redcarpet
  renderer = Redcarpet::Render::HTML.new
  markdown = Redcarpet::Markdown.new(renderer, {
    tables: true,
    autolink: true,
    fenced_code_blocks: true
  })

  # Walk through Markdown files
  Dir.glob(File.join(MARKDOWN_DIR, "**/*.md")).each do |file|
    relative_path = Pathname.new(file).relative_path_from(Pathname.new(MARKDOWN_DIR)).to_s
    current_folder = File.dirname(relative_path) # Get the folder for relative links
    output_file = relative_path.sub(/\.md$/, ".html")
    FileUtils.mkdir_p(File.dirname(output_file))

    # Read and parse Markdown file
    md_content = File.read(file)
    front_matter, body_content = parse_front_matter(md_content, defaults)

    # Handle handlebars in content
    body_content = replace_custom_handlebars(body_content)

    # Convert Markdown to HTML
    html_body = markdown.render(body_content)
    html_body = update_image_links(html_body)
    html_body = convert_links_to_html(html_body, current_folder) # Pass folder context

    # Add meta tags and menu
    meta_tags = generate_meta_tags(front_matter)
    menu = generate_menu(front_matter)

    # Add title, author, date, and summary
    header_content = ""
    header_content << "<h1>#{front_matter['title']}</h1>" if front_matter['title']
    header_content << "<h2>By #{front_matter['author']} on #{front_matter['date']}</h2>" if front_matter['author'] && front_matter['date']
    header_content << "<h3>#{front_matter['summary']}</h3>" if front_matter['summary']
    header_content << <<~HTML if front_matter["image"]
      <img src="/#{front_matter['image']}" alt="#{front_matter['title']}">
    HTML

    # Write HTML file
    File.write(output_file, <<~HTML)
      <!DOCTYPE html>
      <html>
      <head>
        <title>#{front_matter['title'] || 'Krems'}</title>
        #{generate_static_asset_links}
        #{meta_tags}
      </head>
      <body>
        #{menu}
        #{header_content}
        #{html_body}
        #{generate_footer}
      </body>
      </html>
    HTML
  end
end

# Ensure default index.md exists
ensure_index_md

# Clean root directory and run conversion
convert_markdown_to_html

# Serve the static site with Sinatra
set :public_folder, "./"

get '/' do
  send_file "index.html"
end

# Keep the Sinatra server running
Sinatra::Application.run!
