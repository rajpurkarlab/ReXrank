import pandas as pd
import math
import json
import html as html_module
import os
from decimal import Decimal, ROUND_DOWN


def generate_rexgroundingct_html(csv_path, output_path, per_category_csv_path=None, category_counts_csv_path=None):
    df = pd.read_csv(csv_path)
    if per_category_csv_path is None:
        per_category_csv_path = os.path.join(os.path.dirname(csv_path), 'per_category_results.csv')
    if category_counts_csv_path is None:
        category_counts_csv_path = os.path.join(os.path.dirname(csv_path), 'category_counts.csv')

    # Format metric values
    def fmt(val):
        if pd.isna(val) or (isinstance(val, float) and math.isnan(val)):
            return '0.000'
        truncated = Decimal(str(float(val))).quantize(Decimal('0.000'), rounding=ROUND_DOWN)
        return f'{truncated:.3f}'

    # Group rows by model name to support multiple submission versions
    # Preserve insertion order: first occurrence determines display order
    from collections import OrderedDict
    model_groups = OrderedDict()
    for _, row in df.iterrows():
        model_name = str(row['Model'])
        if model_name not in model_groups:
            model_groups[model_name] = []
        model_groups[model_name].append(row)

    # Build table rows from grouped models
    rows_html = ''
    for model_name, versions in model_groups.items():
        # Use the first version as the default displayed row
        default = versions[0]
        model_url = str(default.get('Model URL', ''))
        institution = str(default.get('Institution', ''))

        # Model cell: link if URL exists, plain text otherwise
        if model_url and model_url != 'nan' and model_url.strip():
            model_cell = f'<a href="{model_url}" target="_blank">{model_name}</a>'
        else:
            model_cell = model_name

        # Institution line (split onto new lines when multiple institutions are separated by '&')
        if institution and institution != 'nan' and institution.strip():
          institution_parts = [html_module.escape(part.strip()) for part in institution.split('&') if part.strip()]
          institution_display = '<br/>'.join(institution_parts)
          institution_html = f'<p class="institution">{institution_display}</p>'
        else:
            institution_html = '<p class="institution"></p>'

        # Build version data for JS
        versions_data = []
        for v_row in versions:
          version_label = str(v_row.get('Version', '')).strip()
          if version_label == 'nan':
            version_label = ''
          date_val = str(v_row.get('Date', '')) if pd.notna(v_row.get('Date', '')) else ''
          if date_val == 'nan':
              date_val = ''
          versions_data.append({
                'version': version_label,
                'date': date_val,
                'dice': fmt(v_row['Global Dice']),
                'hit': fmt(v_row['Global HIT Rate']),
                'prec': fmt(v_row['Instance Precision']),
                'rec': fmt(v_row['Instance Recall']),
                'f1': fmt(v_row['Instance F1']),
            })

        default_index = len(versions_data) - 1
        default_version = versions_data[default_index]
        has_multiple = len(versions_data) > 1

        # Version selector HTML (only if multiple versions exist)
        if has_multiple:
            version_selector = f'<div class="version-selector" data-versions=\'{html_module.escape(json.dumps(versions_data), quote=True)}\'>'
            version_selector += f'<span class="version-badge"><span class="version-label">{default_version["version"]}</span><svg class="version-caret-icon" width="10" height="6" viewBox="0 0 10 6"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
            version_selector += '<div class="version-dropdown">'
            for i, vd in enumerate(versions_data):
                active_cls = ' active' if i == default_index else ''
                version_selector += f'<div class="version-option{active_cls}" data-index="{i}">{vd["version"]}</div>'
            version_selector += '</div></div>'
        else:
            version_selector = ''

        default_date = default_version.get('date', '')
        date_html = f'<span class="date label label-default model-date">{default_date}</span>' if default_date else '<span class="model-date"></span>'
        rows_html += f'''                  <tr data-model="{html_module.escape(model_name, quote=True)}" data-versions='{html_module.escape(json.dumps(versions_data), quote=True)}' data-current-version="{default_index}">
                    <td style="word-break:break-word;">
                      {model_cell}
                      {institution_html}
                      <div style="display:inline-flex;flex-direction:column;align-items:center;gap:4px;">{date_html}{version_selector}</div>
                    </td>
                    <td class="metric-dice"><b>{default_version["dice"]}</b></td>
                    <td class="metric-hit"><b>{default_version["hit"]}</b></td>
                    <td class="metric-prec"><b>{default_version["prec"]}</b></td>
                    <td class="metric-rec"><b>{default_version["rec"]}</b></td>
                    <td class="metric-f1"><b>{default_version["f1"]}</b></td>
                  </tr>
'''

    # Per-category data (DAGG Submission 2 provided; all others default to 0 for now)
    category_order = [
        '1a', '1b', '1c', '1d', '1e', '1f',
      '2a', '2b', '2c', '2d', '2e', '2f', '2g', '2h'
    ]

    category_labels = {
      '1a': 'Bronchial wall thickening',
      '1b': 'Bronchiectasis',
      '1c': 'Emphysema (including Centrilobular, Paraseptal, Bullous)',
      '1d': 'Septal thickening (including Interlobular, Reticulation)',
      '1e': 'Micronodules (including Centrilobular, Tree-in-bud, Perilymphatic)',
      '1f': 'Other',
      '2a': 'Linear (including subsegmental atelectasis, scarring, fibrosis)',
      '2b': 'Atelectasis, consolidation',
      '2c': 'Groundglass opacity',
      '2d': 'Pulmonary nodules/masses',
      '2e': 'Pleural effusion or thickening',
      '2f': 'Honeycombing',
      '2g': 'Pneumothorax',
      '2h': 'Other',
    }

    model_versions = {}
    for model_name, versions in model_groups.items():
        labels = []
        for v_row in versions:
            version_label = str(v_row.get('Version', '')).strip()
            if version_label == 'nan':
                version_label = ''
            if version_label not in labels:
                labels.append(version_label)
        model_versions[model_name] = labels

    category_counts = {cat: 0 for cat in category_order}
    if os.path.exists(category_counts_csv_path):
      category_counts_df = pd.read_csv(category_counts_csv_path)
      required_count_cols = {'Category', 'n'}
      if required_count_cols.issubset(set(category_counts_df.columns)):
        for _, row in category_counts_df.iterrows():
          category_code = str(row.get('Category', '')).strip()
          if category_code in category_counts:
            try:
              category_counts[category_code] = int(float(row.get('n', 0)))
            except Exception:
              category_counts[category_code] = 0

    per_category_lookup = {}
    for model_name, labels in model_versions.items():
        for label in labels:
            key = f'{model_name}|||{label}'
            per_category_lookup[key] = {
                cat: {'n': category_counts.get(cat, 0), 'dice': '0.000', 'hit': '0.000'}
                for cat in category_order
            }

    if os.path.exists(per_category_csv_path):
      per_category_df = pd.read_csv(per_category_csv_path)
      required_cols = {'Model', 'Version', 'Category', 'Dice', 'Hit Rate'}
      if required_cols.issubset(set(per_category_df.columns)):
        for _, row in per_category_df.iterrows():
          model_name = str(row.get('Model', '')).strip()
          version_label = str(row.get('Version', '')).strip()
          if version_label == 'nan':
            version_label = ''
          category_code = str(row.get('Category', '')).strip()
          key = f'{model_name}|||{version_label}'
          if key in per_category_lookup and category_code in per_category_lookup[key]:
            per_category_lookup[key][category_code] = {
              'n': per_category_lookup[key][category_code]['n'],
              'dice': fmt(row.get('Dice', 0)),
              'hit': fmt(row.get('Hit Rate', 0)),
            }

    # Sort models by hit rate (highest first); find max hit rate across all versions
    model_hit_rates = []
    for model_name, versions in model_groups.items():
        max_hit_rate = 0
        for v_row in versions:
            hit_rate = float(v_row.get('Global HIT Rate', 0))
            if hit_rate > max_hit_rate:
                max_hit_rate = hit_rate
        model_hit_rates.append((model_name, max_hit_rate))
    model_hit_rates.sort(key=lambda x: x[1], reverse=True)

    model_options_html = ''
    for model_name, _ in model_hit_rates:
        escaped_name = html_module.escape(model_name)
        model_options_html += f'<option value="{escaped_name}">{escaped_name}</option>'

    default_category_model = model_hit_rates[0][0] if model_hit_rates else 'DAGG'

    html = f'''<!DOCTYPE html>
<!--Author: Xiaoman Zhang 2024 -->
<html>
<head>
  <meta charset="utf-8"/>
  <title>
    ReXGroundingCT
  </title>
  <meta name="description" content="ReXGroundingCT: A large-scale 3D chest CT dataset linking free-text radiology findings to pixel-level segmentations in volumetric imaging."/>
  <meta name="keywords" content="ReXGroundingCT, radiology, chest CT, segmentation, medical imaging"/>
  <meta property="og:title" content="ReXGroundingCT: 3D Chest CT Dataset"/>
  <meta property="og:description" content="A large-scale 3D chest CT dataset linking free-text radiology findings to pixel-level segmentations in volumetric imaging."/>
  <meta property="og:url" content="https://rajpurkarlab.github.io/ReXrank/rexgroundingct/"/>
  <meta property="og:type" content="website"/>
  <html lang="en"></html>
  <meta content="ReXGroundingCT is a large-scale 3D chest CT dataset linking free-text radiology findings to pixel-level segmentations in volumetric imaging." name="description"/>
  <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
  <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport"/>
  <meta content="/logo.png" property="og:image"/>
  <link href="../logo.png" rel="image_src" type="image/png"/>
  <link href="../favicon.ico" rel="shortcut icon" type="image/x-icon"/>
  <link href="../favicon.ico" rel="icon" type="image/x-icon"/>
  <link href="../bower_components/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <link href="../stylesheets/layout.css" rel="stylesheet"/>
  <link href="../stylesheets/index.css" rel="stylesheet"/>
  <script src="../javascripts/analytics.js"></script>
  <script src="../bower_components/jquery/dist/jquery.min.js"></script>
  <script src="../javascripts/jquery.tablesorter.min.js"></script>
  <link rel="stylesheet" href="../stylesheets/theme.default.min.css">

  <script async="" defer="" src="https://buttons.github.io/buttons.js"></script>

  <style>
    .fixed-height-table {{
      height: 300px; /* Fixed height, adjust as needed */
      overflow-y: scroll;
      display: block;
    }}
    .fixed-height-table thead {{
      position: sticky;
      top: 0;
      background-color: white; /* Table header background color */
      z-index: 1;
    }}
    .fixed-height-table th, .fixed-height-table td {{
      padding: 8px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }}
    .justified-text {{
      text-align: justify;
      text-justify: inter-word;
    }}
  </style>
  <style>
    .performanceTable th {{
      cursor: pointer;
    }}
    #contentCover .performanceTable th,
    #contentCover .performanceTable td,
    #contentCover .performanceTable.tablesorter td,
    #contentCover .performanceTable.tablesorter th,
    #contentCover .categoryTable th,
    #contentCover .categoryTable td {{
      text-align: center !important;
      vertical-align: middle !important;
    }}
    #contentCover .categoryTable td:first-child,
    #contentCover .categoryTable th:first-child {{
      text-align: left !important;
    }}
    .category-controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 12px;
    }}
    .category-control-item {{
      min-width: 220px;
    }}
    .category-control-item label {{
      display: block;
      margin-bottom: 4px;
      font-weight: 600;
      font-size: 13px;
    }}
    .categoryTable th {{
      font-weight: 700;
    }}
    /* Version selector styles */
    .version-selector {{
      position: relative;
      display: inline-block;
      margin-top: 4px;
    }}
    .model-date {{
      margin-top: 0;
    }}
    .version-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 11px;
      padding: 2px 10px;
      background: linear-gradient(135deg, #f7f7f9, #eef0f3);
      border: 1px solid #d0d3d9;
      border-radius: 4px;
      cursor: pointer;
      color: #555;
      white-space: nowrap;
      user-select: none;
      transition: all 0.2s ease;
      font-weight: 500;
      letter-spacing: 0.3px;
    }}
    .version-badge:hover {{
      background: linear-gradient(135deg, #eef0f3, #e2e5ea);
      border-color: #a41034;
      color: #a41034;
      box-shadow: 0 1px 3px rgba(164,16,52,0.12);
    }}
    .version-caret-icon {{
      flex-shrink: 0;
      transition: transform 0.2s ease;
    }}
    .version-selector:hover .version-caret-icon {{
      transform: rotate(180deg);
    }}
    .version-dropdown {{
      display: none;
      position: absolute;
      top: 100%;
      left: 0;
      z-index: 100;
      background: #fff;
      border: 1px solid #d0d3d9;
      border-radius: 4px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      min-width: 70px;
      padding: 4px 0;
      animation: versionDropIn 0.15s ease;
    }}
    /* Invisible bridge so mouse doesn't lose hover between badge and dropdown */
    .version-dropdown::before {{
      content: '';
      position: absolute;
      top: -6px;
      left: 0;
      right: 0;
      height: 6px;
    }}
    @keyframes versionDropIn {{
      from {{ opacity: 0; transform: translateY(-4px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .version-selector:hover .version-dropdown {{
      display: block;
    }}
    .version-option {{
      display: block;
      padding: 5px 14px;
      font-size: 12px;
      cursor: pointer;
      color: #444;
      white-space: nowrap;
      transition: all 0.12s ease;
      border-left: 2px solid transparent;
    }}
    .version-option:hover {{
      background: #fdf2f4;
      color: #a41034;
      border-left-color: #a41034;
    }}
    .version-option.active {{
      font-weight: 600;
    }}
  </style>
  <style>
    /* Dropdown hover functionality */
    .navbar-nav .dropdown:hover .dropdown-menu {{
      display: block;
    }}
    .navbar-nav .dropdown-menu {{
      margin-top: 0;
      background-color: #fff !important;
    }}
    /* Fix dropdown menu colors */
    #topNavbar .navbar-nav .dropdown-menu > li > a,
    #topNavbar .navbar-nav .dropdown-menu > li > a:hover,
    #topNavbar .navbar-nav .dropdown-menu > li > a:focus,
    #topNavbar .navbar-right .dropdown-menu > li > a,
    #topNavbar .navbar-right .dropdown-menu > li > a:hover,
    #topNavbar .navbar-right .dropdown-menu > li > a:focus {{
      color: #333 !important;
      background-color: #fff !important;
    }}
    #topNavbar .navbar-nav .dropdown-menu > li > a:hover,
    #topNavbar .navbar-right .dropdown-menu > li > a:hover {{
      background-color: #f5f5f5 !important;
      color: #a41034 !important;
    }}
  </style>
</head>
<body class="has-banner">
  <div class="navbar navbar-default navbar-fixed-top" id="topNavbar" role="navigation">
    <div class="container clearfix" id="navContainer">
      <div class="rightNav">
        <div class="collapseDiv">
          <button aria-controls="navbar" aria-expanded="false" class="navbar-toggle collapsed" data-target="#navbar" data-toggle="collapse" type="button">
            <span class="glyphicon glyphicon-menu-hamburger"></span>
          </button>
        </div>
        <div class="collapse navbar-collapse" id="navbar">
          <ul class="nav navbar-nav navbar-right">
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false" style="font-size: 18px;">
                ReXrankCT <span class="caret"></span>
              </a>
              <ul class="dropdown-menu">
                <li><a href="../ReXGroundingCT/index.html">ReXGroundingCT</a></li>
              </ul>
            </li>
            <li>
              <a href="../ReX-MLE/index.html" style="font-size: 18px;">ReX-MLE</a>
            </li>
          </ul>
        </div>
      </div>
      <div class="leftNav">
        <div class="brandDiv">
          <a class="navbar-brand" href="../">ReXrank</a>
        </div>
      </div>
    </div>
  </div>
  <div class="challenge-banner">
    🏆 <strong>ReXGroundingCT Challenge @ MICCAI 2026</strong> — Pre-registration is open! <a href="../ReXGroundingCT/challenge.html">Learn More &rarr;</a>
  </div>
  <div class="cover" id="topCover">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h1 id="appTitle">ReXGroundingCT</h1>
          <h2 id="appSubtitle">Segmentation of Findings from Free-Text Reports</h2>
          <h3 id="helpLink"><a href="../explore/submission_guideline_ct.html" target="_blank" rel="noopener noreferrer">⭐@Researchers: Submit to ReXrankCT</a></h3>
          <h3 id="helpLink"><a href="https://arxiv.org/abs/2507.22030" target="_blank" rel="noopener noreferrer">Read the Paper</a></h3>
        </div>
      </div>
    </div>
  </div>
  <div class="cover" id="contentCover">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <div class="infoCard">
            <div class="infoBody justified-text">
              <div class="infoHeadline">
                <h2>About ReXGroundingCT</h2>
              </div>
              <p>ReXGroundingCT is a large-scale 3D chest CT dataset linking free-text radiology findings to pixel-level segmentations in volumetric imaging. It comprises 3,142 non-contrast chest CT scans with 8,028 annotated findings (16,301 entities) from the CT-RATE dataset. ReXGroundingCT enables sentence-level grounding for both focal and non-focal lung and pleural abnormalities across 14 categories. On ReXrank, we are hosting ReXGroundingCT's testset, which contains 100 CT scans with exhaustive radiologist annotations for all visible findings.</p>
              <hr>
              <div class="infoHeadline">
                <h2>Performance Metrics</h2>
              </div>
              <p><strong>Global Dice:</strong> Average Dice per finding per case</p>
              <p><strong>Global HIT Rate:</strong> Proportion of findings that have Dice >= 0.1</p>
              <p><strong>Instance Precision:</strong> TP / (TP + FP), where True Positives are instances that have a Dice >= 0.2</p>
              <p><strong>Instance Recall:</strong> TP / (TP + FN)</p>
              <hr>
              <div class="infoHeadline">
                <h2>Model Performance</h2>
              </div>
              <table class="table performanceTable tablesorter">
                <thead>
                  <tr>
                    <th>Model</th>
                    <th>Global Dice</th>
                    <th>Global HIT Rate</th>
                    <th>Instance Precision</th>
                    <th>Instance Recall</th>
                    <th>Instance F1</th>
                  </tr>
                </thead>
                <tbody>
{rows_html}                </tbody>
              </table>
              <hr>
              <div class="infoHeadline">
                <h2>Per-Category Results</h2>
              </div>
              <div class="category-controls">
                <div class="category-control-item">
                  <label for="categoryModelSelect">Model</label>
                  <select id="categoryModelSelect" class="form-control">
                    {model_options_html}
                  </select>
                </div>
                <div class="category-control-item" id="categorySubmissionControl">
                  <label for="categorySubmissionSelect">Submission</label>
                  <select id="categorySubmissionSelect" class="form-control"></select>
                </div>
              </div>
              <table class="table categoryTable">
                <thead>
                  <tr>
                    <th>Category</th>
                    <th>n</th>
                    <th>Dice</th>
                    <th>Hit Rate</th>
                  </tr>
                </thead>
                <tbody id="categoryTableBody"></tbody>
              </table>
              <p><strong>Legend:</strong> Category codes starting with <strong>1</strong> are typically non-focal lung/airway/pleural abnormalities; codes starting with <strong>2</strong> are typically focal lung/airway/pleural opacities.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    $(document).ready(function() {{
      $(".performanceTable").tablesorter({{
        sortList: [[2, 1]]
      }});

      var modelVersions = {json.dumps(model_versions)};
      var categoryOrder = {json.dumps(category_order)};
      var categoryLabels = {json.dumps(category_labels)};
      var perCategoryLookup = {json.dumps(per_category_lookup)};
      var defaultCategoryModel = {json.dumps(default_category_model)};

      function renderCategorySubmissionOptions(modelName, preferredVersion) {{
        var versions = modelVersions[modelName] || [];
        var $submissionSelect = $("#categorySubmissionSelect");
        var $submissionControl = $("#categorySubmissionControl");
        $submissionSelect.empty();

        if (versions.length <= 1) {{
          $submissionControl.hide();
        }} else {{
          $submissionControl.show();
        }}

        versions.forEach(function(versionLabel) {{
          $submissionSelect.append(
            $("<option></option>").val(versionLabel).text(versionLabel)
          );
        }});

        var selectedVersion = '';
        if (preferredVersion && versions.indexOf(preferredVersion) !== -1) {{
          selectedVersion = preferredVersion;
        }} else if (versions.length > 0) {{
          selectedVersion = versions[versions.length - 1];
        }}

        $submissionSelect.val(selectedVersion);
        return selectedVersion;
      }}

      function renderCategoryTable(modelName, versionLabel) {{
        var key = modelName + "|||" + versionLabel;
        var categoryData = perCategoryLookup[key] || {{}};
        var rows = '';

        categoryOrder.forEach(function(categoryCode) {{
          var item = categoryData[categoryCode] || {{ n: 0, dice: '0.000', hit: '0.000' }};
          var categoryLabel = categoryLabels[categoryCode] || '';
          var categoryCell = '<b>' + categoryCode + '</b>' + (categoryLabel ? ' — ' + categoryLabel : '');
          rows += '<tr>' +
            '<td>' + categoryCell + '</td>' +
            '<td>' + item.n + '</td>' +
            '<td>' + item.dice + '</td>' +
            '<td>' + item.hit + '</td>' +
            '</tr>';
        }});

        $("#categoryTableBody").html(rows);
      }}

      if (defaultCategoryModel) {{
        $("#categoryModelSelect").val(defaultCategoryModel);
        var initialSubmission = renderCategorySubmissionOptions(defaultCategoryModel);
        renderCategoryTable(defaultCategoryModel, initialSubmission);
      }}

      $("#categoryModelSelect").on("change", function() {{
        var selectedModel = $(this).val();
        var selectedSubmission = renderCategorySubmissionOptions(selectedModel);
        renderCategoryTable(selectedModel, selectedSubmission);
      }});

      $("#categorySubmissionSelect").on("change", function() {{
        var selectedModel = $("#categoryModelSelect").val();
        var selectedSubmission = $(this).val();
        renderCategoryTable(selectedModel, selectedSubmission);
      }});

      // Custom sort handler: always start descending on a new column,
      // only toggle if clicking the same column consecutively
      var lastCol = 2;
      var lastDir = 1; // 1 = desc, 0 = asc

      // Remove tablesorter's default click handlers on headers
      $(".performanceTable thead th").off("click mousedown");

      $(".performanceTable thead th").on("click", function(e) {{
        e.stopPropagation();
        var col = $(this).index();
        var dir;
        if (col === lastCol) {{
          dir = lastDir === 1 ? 0 : 1; // toggle
        }} else {{
          dir = 1; // always descending for a new column
        }}
        lastCol = col;
        lastDir = dir;
        $(".performanceTable").trigger("sorton", [[[col, dir]]]);
      }});

      // Version switching logic
      $(document).on('click', '.version-option', function(e) {{
        e.stopPropagation();
        var $option = $(this);
        var versionIndex = parseInt($option.data('index'));
        var $row = $option.closest('tr');
        var versions = $row.data('versions');

        if (!versions || versionIndex >= versions.length) return;

        var selected = versions[versionIndex];

        // Update scores
        $row.find('.metric-dice b').text(selected.dice);
        $row.find('.metric-hit b').text(selected.hit);
        $row.find('.metric-prec b').text(selected.prec);
        $row.find('.metric-rec b').text(selected.rec);
        $row.find('.metric-f1 b').text(selected.f1);

        // Update date
        var $dateSpan = $row.find('.model-date');
        if (selected.date) {{
          $dateSpan.text(selected.date).addClass('date label label-default');
        }} else {{
          $dateSpan.text('').removeClass('date label label-default');
        }}

        // Update active state
        $option.siblings().removeClass('active');
        $option.addClass('active');

        // Update badge label
        $row.find('.version-label').text(selected.version);

        // Store current version
        $row.attr('data-current-version', versionIndex);

        // Sync per-category viewer if this model is selected there
        var currentModelInViewer = $("#categoryModelSelect").val();
        var rowModel = String($row.data('model') || '');
        if (currentModelInViewer === rowModel) {{
          $("#categorySubmissionSelect").val(selected.version);
          renderCategoryTable(rowModel, selected.version);
        }}

        // Re-trigger tablesorter update
        $(".performanceTable").trigger("update");
      }});
    }});
  </script>
</body>
</html>
'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Generated {output_path} from {csv_path}')


if __name__ == '__main__':
    generate_rexgroundingct_html(
        './ReXGroundingCT/ReXGroundingCT.csv',
    './ReXGroundingCT/index.html',
    './ReXGroundingCT/per_category_results.csv'
    )
