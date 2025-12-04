---
title: "Krems static blog generator"
author: "Matt Reider"
date: "2025-02-16"
image: "/images/matt/gh-krems.png"
---

A couple of months ago we visited a little town named Krems about an hour West of Vienna. In that little town is a University where my son would apply, though now that he’s been accepted to a few schools in Scotland he likely won’t attend. After we returned to Vienna I thought about writing a short blog about our visit there, but to my horror my blog was nolonger loading properly.

Instead of adjusting my hugo templates for the 1,000th time, I decided to write my own static blog generator for Github Pages. I named it Krems after the cute little town we visited.

Unlike Hugo, or Jekyll, Krems has almost no customability. It’s dead simple, has only one theme, and does exactly what it does, with nothing more.

1. Runs as a simple executable on most operating systems
2. Generates HTML pages from Markdown
3. Creates slug links instead of pages with “.html” file extensions
4. Generates index pages of blog entries based on the contents of a folder
5. Creates simple responsive menus
6. Runs an http server locally for testing purposes

Here’s how you use it:

# Install Krems

Download the latest binary for your operating system at [Releases · mreider/krems](https://github.com/mreider/krems/releases). On my mac I give it executable privileges and put it in my path.

```bash
curl -L https://github.com/mreider/krems/releases/download/v0.1.9/krems-darwin-amd64 -o krems
chmod +x krems
mv krems /usr/local/bin/
```
 
# Create a sample site

To create a sample site with folders, pages, and configurations, run:

```bash
mkdir test
cd test
krems --init
```

This will generate the following structure:

```
markdown/images/ <-- images saved here
markdown/ <-- markdown saved here
markdown/css/bootstrap.min.css
markdown/js/bootstrap.js
config.yaml
```

Next, build the site by running:

```bash
krems --build
```

This creates a docs folder and generates HTML from the Markdown files while copying necessary assets like CSS, JS, and images. The resulting folder structure looks like this:

```bash
docs/ <-- html pages generated from markdown here
docs/CNAME <-- creates a domain from config.yaml
docs/rss.xml
docs/404.html
docs/images
docs/css
docs/js
```

Finally, you can run the website locally by running `krems  -run`.

# Exploring the demo site

The demo site starts with an index page that lists subpages in the same directory:

![krems demo index](/images/matt/krems-test.png)

Clicking the first links takes us to the Krems City Info page:

![krems info page](/images/matt/krems-test2.png)

You can also go to menu and see info about the universities in Krems:

![krems uni page](/images/matt/krems-test3.png)

# Understanding the structure

Now that you’ve explored the demo site, let's look at its structure. Open the index page `markdown/index.md` in a text editor. You'll see:

```yaml
---
title: "Krems Home Page"
type: list
---
```

This is a list page. It has no content, only front matter. List pages automatically generate a list of links to HTML pages in the same directory. In this case, there are two other pages.

Since Krems is designed for blogs, not traditional websites, a list page only includes links to pages that have dates in their front matter. If you don’t want a file to appear in the list, simply omit the date.

Other pages use the default "normal" type, meaning there's no need to specify it explicitly. Here’s an example of the Krems City Info page:


```yaml
---
title: "Krems City Info"
date: "2024-11-26"
image: "/images/krems1.png"
---
Krems is a beautiful city in Austria known for its rich history, stunning architecture, and vibrant culture.

Explore its winding streets, local markets, and historical landmarks.
```

This page includes an image in the front matter. When converted to HTML, the image is automatically placed above the page title with a small border, a maximum width of 600px, and responsive resizing for different screen sizes. If you share the page on social media (e.g., LinkedIn), this image will appear as the preview.

The last key component is the `config.yaml` file, which defines the site’s domain and menu structure:


```yaml
website:
  url: "http://localhost:8080"
  name: "Krems Static Site"

menu:
  - title: "Home"
    path: "index.md"
  - title: "Universities"
    path: "universities/index.md"
```

This is pretty self-explanatory. Replace the url with your actual blog domain and modify the menu, pages, and images as needed.

# Publishing to Github Pages

Once you've built your blog by running:

```bash
krems --build
```

all the generated HTML files will be in the docs folder, exactly where GitHub Pages expects them. A CNAME file will also be created in docs/, allowing you to set up a custom domain.

Setting up Github Pages is pretty straightforward but Github's documentation is not great. 

1. Create a GitHub repository for your Krems site.
2. Add everything to the repo, including the /markdown and /docs folders.
3. In your repository, go to Settings → Pages and configure it like this:

![gh pages settings](/images/matt/gh-pages-build.png)

To use a custom domain follow Github's [guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages).

# Final thoughts

If you run into issues with Krems or have feature suggestions, feel free to use the [Issues section in the GitHub repo](https://github.com/mreider/krems/issues).

If you'd like to contribute, especially by improving the auto-generated CSS template (which currently just uses Bootstrap), that would be a nice enhancement.


