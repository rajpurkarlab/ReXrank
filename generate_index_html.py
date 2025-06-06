def generate_html(table_chexpertplus_html, table_iuxray_html, table_mimiccxr_html, table_private_html, table_rank_v1_html, table_rank_v2_html, table_vqa_html, save_html_path):
    head_html = '''<!DOCTYPE html>
<!--Author: Xiaoman Zhang 2024 -->
<html>
<head>
  <meta charset="utf-8"/>
  <title>
    ReXrank
  </title>
  <meta name="google-site-verification" content="nhtTEYeNrlo4w3RA5TuRR338uGFQGDhhSYAFEBA301c" />
  <meta name="description" content="ReXrank: The leading open-source leaderboard for radiology report generation. Compare and benchmark AI models for medical imaging reports."/>
  <meta name="keywords" content="ReXrank, radiology, report generation, AI, medical imaging, leaderboard, benchmarking"/>
  <meta property="og:title" content="ReXrank: Radiology Report Generation Leaderboard"/>
  <meta property="og:description" content="Open-source leaderboard for comparing and benchmarking AI models in radiology report generation."/>
  <meta property="og:url" content="https://rajpurkarlab.github.io/ReXrank/"/>
  <meta property="og:type" content="website"/>
  <html lang="en"></html>
  <meta content="ReXrank is an open-source leaderboard for AI-powered radiology report generation from chest x-ray images." name="description"/>
  <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
  <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport"/>
  <meta content="/logo.png" property="og:image"/>
  <link href="./logo.png" rel="image_src" type="image/png"/>
  <link href="./favicon.ico" rel="shortcut icon" type="image/x-icon"/>
  <link href="./favicon.ico" rel="icon" type="image/x-icon"/>
  <link href="./bower_components/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <link href="./stylesheets/layout.css" rel="stylesheet"/>
  <link href="./stylesheets/index.css" rel="stylesheet"/>
  <script src="./javascripts/analytics.js"></script>
  <script src="./bower_components/jquery/dist/jquery.min.js"></script>
  <script src="./javascripts/jquery.tablesorter.min.js"></script>
  <link rel="stylesheet" href="./stylesheets/theme.default.min.css">

  <script async="" defer="" src="https://buttons.github.io/buttons.js"></script>
  <link rel="canonical" href="https://rexrank.azurewebsites.net/" />

  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "ReXrank",
      "description": "Open-source leaderboard for radiology report generation",
      "url": "https://rajpurkarlab.github.io/ReXrank/",
      "keywords": ["ReXrank", "radiology", "report generation", "chest x-ray", "leaderboard", "benchmarking"]      
    }
  </script>

  <style>
    .fixed-height-table {
      height: 300px; /* 固定高度，可根据需要调整 */
      overflow-y: scroll;
      display: block;
    }
    .fixed-height-table thead {
      position: sticky;
      top: 0;
      background-color: white; /* 表头背景色 */
      z-index: 1;
    }
    .fixed-height-table th, .fixed-height-table td {
      padding: 8px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    .justified-text {
      text-align: justify;
      text-justify: inter-word;
    }
  </style>
  <style>
    .performanceTable th {
      cursor: pointer;
    }
  </style>
</head>
<body>
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
            <li>
              <a href="./" style="font-size: 18px;">Home</a>
            </li>
            <!-- <li>
              <a href="./explore/vote_example.html" style="font-size: 18px;">Arena</a>
            </li>
            <li>
              <a href="./explore/login.html" style="font-size: 18px;">Login</a>
            </li> -->
          </ul>
        </div>
      </div>
      <div class="leftNav">
        <div class="brandDiv">
          <a class="navbar-brand" href="./">ReXrank</a>
        </div>
      </div>
    </div>
  </div>
  <div class="cover" id="topCover">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h1 id="appTitle">ReXrank</h1>
          <h2 id="appSubtitle">Chest X-ray Interpretation Leaderboard</h2>
          <!-- <h3 id="helpLink"><a href="https://github.com/rajpurkarlab/ReXrank/blob/main/example_files/submission_tutorial.md" target="_blank" rel="noopener noreferrer">⭐@Researchers: Submit to ReXrank</a></h3>
          <p><a href="https://forms.gle/qNUXgXpmDnhUprjF8" target="_blank" rel="noopener noreferrer">Wanna help us?</a></p> -->
        </div>
      </div>
    </div>
  </div>
  <div class="cover" id="contentCover">
    <div class="container">
      <div class="row">
        <div class="col-md-5">
          <div class="infoCard">
            <div class="infoBody justified-text">
              <div class="infoHeadline">
                <h2>What is ReXrank?</h2>
              </div>
              <p><b>ReXrank</b> is a public leaderboard for chest X-ray image interpretation, including both radiology report generation (RRG) and visual question answering (VQA) tasks. 
              <hr>
              <p><b>ReXrank Challenge V1.0</b> is a competition in the generation of chest radiograph reports utilizing ReXGradient, the largest private test dataset consisting of 10,000 studies across 67 sites. The challenge attracted diverse participants from academic institutions, industry, and independent research teams, resulting in 24 state-of-the-art models previously benchmarked. </p>   
             <hr>
              <p><b>ReXrank Challenge V2.0</b> is a competition in VQA task utilizing VQA dataset constructed from ReXGradient, including 41,007 VQA pairs with 10,000 radiological studies. We benchmarked 8 state-of-the-art models. </p>
              <hr>
              <p><a href="https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K" target="_blank">ReXGradient-160K</a>  is the largest publicly available multi-site chest X-ray dataset, containing 273,004 unique chest X-ray images from 160,000 radiological studies, collected from 109,487 unique patients across 3 U.S. health systems (79 medical sites). In ReXrank, we use additional private test set ReXGradient, 10,000 studies for benchmarking.</p>
              <hr>
              <p><a href="https://huggingface.co/datasets/rajpurkarlab/ReXVQA" target="_blank">ReXVQA</a> is the largest and most comprehensive benchmark for VQA in chest radiology, comprising 653834 questions paired with 160,000 radiological studies. The dataset is constructed from ReXGradient-160K.</p>
              </div>
            </div>
        </div>'''
    mid_html = '''{table_rank_v1_html} {table_rank_v2_html} {table_private_html} {table_mimiccxr_html} {table_iuxray_html} {table_chexpertplus_html} {table_vqa_html}  '''.format(table_chexpertplus_html=table_chexpertplus_html, table_iuxray_html=table_iuxray_html, table_mimiccxr_html=table_mimiccxr_html, table_private_html= table_private_html, table_rank_v1_html=table_rank_v1_html, table_rank_v2_html=table_rank_v2_html, table_vqa_html=table_vqa_html)
    tail_html = '''
        </div>
        </div>
    </div>
    <nav class="navbar navbar-default navbar-static-bottom footer">
        <div class="container clearfix">
        <div class="rightNav">
            <div>
            <ul class="nav navbar-nav navbar-right">
                <li>
                <a href="/ReXrank/">ReXrank</a>
                </li>
                <li>
                <a href="https://www.rajpurkarlab.hms.harvard.edu/">Harvard Rajpurkar Lab</a>
                </li>
            </ul>
            </div>
        </div>
        </div>
    </nav>
    <script src="/ReXrank/bower_components/jquery/dist/jquery.min.js"></script>
    <script src="/ReXrank/javascripts/jquery.tablesorter.min.js"></script>
    <script src="/ReXrank/bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
     <script>
        $(document).ready(function() {
            // Initialize tablesorter
            $("#modelTableTest").tablesorter({
                theme: 'default',
                headers: {
                    0: { sorter: false }, // Rank column
                    1: { sorter: false }  // Model column
                },
                sortList: [[2, 1]] // Default sort by RadCliQ-v1 ascending
            });
    
            // Update ranks after sorting
            function updateRankTest() {
                $("#modelTableTest tbody:visible tr").each(function(index) {
                    $(this).find("td:eq(0) p").text(index + 1);
                });
            }
            
            // Function to sort table based on custom order for clicked column
            function customSortTest(columnIndex) {
                var sortOrder = [1,1,1,1,1,1,1,1]; // 示例排序顺序数组
                var sortDirection = sortOrder[columnIndex - 2]; // 获取点击列对应的排序方向
                $("#modelTableTest").trigger("sorton", [[[columnIndex, sortDirection]]]);
            }

            // Detect column header click and apply custom sort
            $("#modelTableTest th").click(function() {
                var columnIndex = $(this).index();
                if (columnIndex > 1) { // 只对第2列及之后的列进行排序
                    customSortTest(columnIndex);
                }
            });

            // Update ranks after table sort ends
            $("#modelTableTest").bind("sortEnd", function() {
              updateRankTest();
            });
    
            // Update ranks on page load
            updateRankTest();
            
            // Initialize tablesorter
            $("#modelTableVQA").tablesorter({
                theme: 'default',
                headers: {
                    0: { sorter: false }, // Rank column
                    1: { sorter: false }  // Model column
                },
                sortList: [[2, 1]] // Default sort by RadCliQ-v1 ascending
            });
    
            // Update ranks after sorting
            function updateRankVQA() {
                $("#modelTableVQA tbody:visible tr").each(function(index) {
                    $(this).find("td:eq(0) p").text(index + 1);
                });
            }
            
            // Function to sort table based on custom order for clicked column
            function customSortTest(columnIndex) {
                var sortOrder = [1,1,1,1,1,1,1,1]; // 示例排序顺序数组
                var sortDirection = sortOrder[columnIndex - 2]; // 获取点击列对应的排序方向
                $("#modelTableVQA").trigger("sorton", [[[columnIndex, sortDirection]]]);
            }

            // Detect column header click and apply custom sort
            $("#modelTableVQA th").click(function() {
                var columnIndex = $(this).index();
                if (columnIndex > 1) { // 只对第2列及之后的列进行排序
                    customSortTest(columnIndex);
                }
            });

            // Update ranks after table sort ends
            $("#modelTableVQA").bind("sortEnd", function() {
              updateRankVQA();
            });
    
            // Update ranks on page load
            updateRankVQA();


            // Initialize tablesorter
            $("#modelTableIU").tablesorter({
                theme: 'default',
                headers: {
                    0: { sorter: false }, // Rank column
                    1: { sorter: false }  // Model column
                },
                sortList: [[2, 1]] // Default sort by RadCliQ-v1 ascending
            });
    
            // Update ranks after sorting
            function updateRanksIU() {
                $("#modelTableIU tbody:visible tr").each(function(index) {
                    $(this).find("td:eq(0) p").text(index + 1);
                });
            }

            // Function to sort table based on custom order for clicked column
            function customSortIU(columnIndex) {
                var sortOrder = [1,1,1,1,1,1,1,1]; // 示例排序顺序数组
                var sortDirection = sortOrder[columnIndex - 2]; // 获取点击列对应的排序方向
                $("#modelTableIU").trigger("sorton", [[[columnIndex, sortDirection]]]);
            }

            // Detect column header click and apply custom sort
            $("#modelTableIU th").click(function() {
                var columnIndex = $(this).index();
                if (columnIndex > 1) { // 只对第2列及之后的列进行排序
                  customSortIU(columnIndex);
                }
            });
    
            // Update ranks after table sort ends
            $("#modelTableIU").bind("sortEnd", function() {
            updateRanksIU();
            });
    
            // Update ranks on page load
            updateRanksIU();
            
            // Initialize tablesorter
            $("#modelTableCheXpert").tablesorter({
                theme: 'default',
                headers: {
                    0: { sorter: false }, // Rank column
                    1: { sorter: false }  // Model column
                },
                sortList: [[2, 1]] // Default sort by RadCliQ-v1 ascending
            });
    
            // Update ranks after sorting
            function updateRanksCheXpert() {
                $("#modelTableCheXpert tbody:visible tr").each(function(index) {
                    $(this).find("td:eq(0) p").text(index + 1);
                });
            }
    
            // Function to sort table based on custom order for clicked column
            function customSortCheXpert(columnIndex) {
                var sortOrder = [1,1,1,1,1,1,1,1]; // 示例排序顺序数组
                var sortDirection = sortOrder[columnIndex - 2]; // 获取点击列对应的排序方向
                $("#modelTableCheXpert").trigger("sorton", [[[columnIndex, sortDirection]]]);
            }

            // Detect column header click and apply custom sort
            $("#modelTableCheXpert th").click(function() {
                var columnIndex = $(this).index();
                if (columnIndex > 1) { // 只对第2列及之后的列进行排序
                  customSortCheXpert(columnIndex);
                }
            });
            // Update ranks after table sort ends
            $("#modelTableCheXpert").bind("sortEnd", function() {
                updateRanksCheXpert();
            });
    
            // Update ranks on page load
            updateRanksCheXpert();

            // Initialize tablesorter
            $("#modelTablePrivate").tablesorter({
                theme: 'default',
                headers: {
                    0: { sorter: false }, // Rank column
                    1: { sorter: false }  // Model column
                },
                sortList: [[2, 1]] // Default sort by RadCliQ-v1 ascending
            });
    
            // Update ranks after sorting
            function updateRanksPrivate() {
                $("#modelTablePrivate tbody:visible tr").each(function(index) {
                    $(this).find("td:eq(0) p").text(index + 1);
                });
            }
    
            // Function to sort table based on custom order for clicked column
            function customSortPrivate(columnIndex) {
                var sortOrder = [1,1,1,1,1,1,1,1]; // 示例排序顺序数组
                var sortDirection = sortOrder[columnIndex - 2]; // 获取点击列对应的排序方向
                $("#modelTablePrivate").trigger("sorton", [[[columnIndex, sortDirection]]]);
            }

            // Detect column header click and apply custom sort
            $("#modelTablePrivate th").click(function() {
                var columnIndex = $(this).index();
                if (columnIndex > 1) { // 只对第2列及之后的列进行排序
                  customSortPrivate(columnIndex);
                }
            });
            // Update ranks after table sort ends
            $("#modelTablePrivate").bind("sortEnd", function() {
                updateRanksPrivate();
            });
    
            // Update ranks on page load
            updateRanksPrivate();

            // Switch to test results
            $("#testBtnIU").click(function() {
                $("#testResultsIU").show();
                $("#validResultsIU").hide();
                $(this).removeClass('btn-gray').addClass('btn-black');
                $("#validBtnIU").removeClass('btn-black').addClass('btn-gray');
                updateRanksIU(); // Update ranks after switching
            });
            $("#testBtnPrivate").click(function() {
                $("#testResultsPrivate").show();
                $("#validResultsPrivate").hide();
                $(this).removeClass('btn-gray').addClass('btn-black');
                $("#validBtnPrivate").removeClass('btn-black').addClass('btn-gray');
                updateRanksPrivate(); // Update ranks after switching
            });
            $("#testBtnCheXpert").click(function() {
                $("#testResultsCheXpert").show();
                $("#validResultsCheXpert").hide();
                $(this).removeClass('btn-gray').addClass('btn-black');
                $("#validBtnCheXpert").removeClass('btn-black').addClass('btn-gray');
                updateRanksCheXpert(); // Update ranks after switching
            });
            $("#testBtnMIMIC").click(function() {
                $("#testResultsMIMIC").show();
                $("#validResultsMIMIC").hide();
                $(this).removeClass('btn-gray').addClass('btn-black');
                $("#validBtnMIMIC").removeClass('btn-black').addClass('btn-gray');
                updateRankTest(); // Update ranks after switching
            });
    
            // Switch to valid results
            $("#validBtnIU").click(function() {
                $("#testResultsIU").hide();
                $("#validResultsIU").show();
                $(this).removeClass('btn-gray').addClass('btn-black');
                $("#testBtnIU").removeClass('btn-black').addClass('btn-gray');
                updateRanksIU(); // Update ranks after switching
            });
            $("#validBtnPrivate").click(function() {
                $("#testResultsPrivate").hide();
                $("#validResultsPrivate").show();
                $(this).removeClass('btn-gray').addClass('btn-black');
                $("#testBtnPrivate").removeClass('btn-black').addClass('btn-gray');
                updateRanksPrivate(); // Update ranks after switching
            });
            $("#validBtnCheXpert").click(function() {
                $("#testResultsCheXpert").hide();
                $("#validResultsCheXpert").show();
                $(this).removeClass('btn-gray').addClass('btn-black');
                $("#testBtnCheXpert").removeClass('btn-black').addClass('btn-gray');
                updateRanksCheXpert(); // Update ranks after switching
            });
            $("#validBtnMIMIC").click(function() {
                $("#testResultsMIMIC").hide();
                $("#validResultsMIMIC").show();
                $(this).removeClass('btn-gray').addClass('btn-black');
                $("#testBtnMIMIC").removeClass('btn-black').addClass('btn-gray');
                updateRankTest(); // Update ranks after switching
            });
          });
          document.addEventListener('DOMContentLoaded', function() {
          const urlParams = new URLSearchParams(window.location.search);
          const message = urlParams.get('message');
          if (message === 'verified' || message === 'already-verified') {
              window.location.href = '/explore/login.html?message=' + message;
          }
        });
    </script>
    
    <style>
        /* .btn {
            margin: 10px;
            padding: 10px 20px;
            color: white;
            border: none;
            cursor: pointer;
        }
        */
        .btn-black {
        background-color: #a41034;
        color: #fff !important;
        border: 2px solid #a41034;
        }
        .btn-gray {
        background-color: #fff;
        color: #a41034 !important;
        border: 2px solid #a41034;
        }

        .btn-black:hover, .btn-gray:hover {
        color: #fff !important;
        } 

        /* .btn-black {
            background-color: black;
        }
    
        .btn-gray {
            background-color: gray;
        }
        
        .btn-black:hover, .btn-gray:hover {
            opacity: 0.8;
        } */
    </style>
    </body>
    </html>
    '''
    return_html = head_html + mid_html + tail_html
    # save the html
    with open(save_html_path, 'w') as f:
        f.write(return_html)


def get_html_content(input_html):
    with open(input_html, 'r') as f:
        return f.read()



table_chexpertplus_html = './results/table_chexpertplus.html'
table_iuxray_html = './results/table_iuxray.html'
table_mimiccxr_html = './results/table_mimiccxr.html'
table_private_html = './results/table_gradienthealth.html'
table_rank_v1_html = './results/table_rank_v1.html'
table_rank_v2_html = './results/table_rank_v2.html'
table_vqa_html = './vqa_results/vqa_results.html'

generate_html(get_html_content(table_chexpertplus_html), get_html_content(table_iuxray_html), get_html_content(table_mimiccxr_html), get_html_content(table_private_html), get_html_content(table_rank_v1_html), get_html_content(table_rank_v2_html), get_html_content(table_vqa_html), save_html_path='./index.html')