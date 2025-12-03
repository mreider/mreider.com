---
title: "Fitness"
---

<style>
.fitness-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.fitness-table th {
  background-color: #f8f9fa;
  padding: 12px 8px;
  text-align: center;
  font-weight: 600;
  border: 1px solid #dee2e6;
  font-size: 14px;
}

.fitness-table td {
  padding: 10px 8px;
  text-align: center;
  border: 1px solid #dee2e6;
  vertical-align: middle;
}

.week-label {
  font-weight: 600;
  background-color: #f8f9fa;
}

.activity-icon {
  font-size: 16px;
  color: #6c757d;
}

.day-cell {
  min-width: 60px;
}

.date-label {
  font-size: 11px;
  color: #6c757d;
  margin-bottom: 6px;
}

.day-box {
  width: 20px;
  height: 20px;
  border-radius: 3px;
  border: 2px solid #e9ecef;
  display: inline-block;
  margin: 0 auto;
}

.day-box.active {
  background-color: #007bff;
  border-color: #007bff;
}
</style>

<table class="fitness-table">
  <thead>
    <tr>
      <th style="width: 60px;">Week</th>
      <th style="width: 40px;"></th>
      <th>Sun</th>
      <th>Mon</th>
      <th>Tue</th>
      <th>Wed</th>
      <th>Thu</th>
      <th>Fri</th>
      <th>Sat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="week-label" rowspan="2">2</td>
      <td class="activity-icon"><i class="fas fa-dumbbell"></i></td>
      <td class="day-cell">
        <div class="date-label">Dec 8</div>
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="date-label">Dec 9</div>
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="date-label">Dec 10</div>
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="date-label">Dec 11</div>
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="date-label">Dec 12</div>
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="date-label">Dec 13</div>
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="date-label">Dec 14</div>
        <div class="day-box"></div>
      </td>
    </tr>
    <tr>
      <td class="activity-icon"><i class="fas fa-apple-alt"></i></td>
      <td class="day-cell">
        <div class="day-box active"></div>
      </td>
      <td class="day-cell">
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="day-box"></div>
      </td>
    </tr>
    <tr>
      <td class="week-label" rowspan="2">1</td>
      <td class="activity-icon"><i class="fas fa-dumbbell"></i></td>
      <td class="day-cell">
        <div class="date-label">Dec 1</div>
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="date-label">Dec 2</div>
        <div class="day-box active"></div>
      </td>
      <td class="day-cell">
        <div class="date-label">Dec 3</div>
        <div class="day-box active"></div>
      </td>
      <td class="day-cell">
        <div class="date-label">Dec 4</div>
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="date-label">Dec 5</div>
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="date-label">Dec 6</div>
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="date-label">Dec 7</div>
        <div class="day-box"></div>
      </td>
    </tr>
    <tr>
      <td class="activity-icon"><i class="fas fa-apple-alt"></i></td>
      <td class="day-cell">
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="day-box active"></div>
      </td>
      <td class="day-cell">
        <div class="day-box active"></div>
      </td>
      <td class="day-cell">
        <div class="day-box"></div>
      </td>
      <td class="day-cell">
        <div class="day-box active"></div>
      </td>
      <td class="day-cell">
        <div class="day-box active"></div>
      </td>
      <td class="day-cell">
        <div class="day-box"></div>
      </td>
    </tr>
  </tbody>
</table>