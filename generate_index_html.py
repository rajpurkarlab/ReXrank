def generate_html(table_chexpertplus_html, table_iuxray_html, table_mimiccxr_html, table_rank_html, save_html_path):
    head_html = '''<!DOCTYPE html>
<!--Author: Xiaoman Zhang 2024 -->
<html>
<head>
  <meta charset="utf-8"/>
  <title>
    ReXrank
  </title>
  <meta content="ReXrank is an open-source leaderboard for radiology report generation." name="description"/>
  <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
  <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport"/>
  <meta content="/logo.png" property="og:image"/>
  <link href="/ReXrank/logo.png" rel="image_src" type="image/png"/>
  <link href="/ReXrank/favicon.ico" rel="shortcut icon" type="image/x-icon"/>
  <link href="/ReXrank/favicon.ico" rel="icon" type="image/x-icon"/>
  <link href="/ReXrank/bower_components/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <link href="/ReXrank/stylesheets/layout.css" rel="stylesheet"/>
  <link href="/ReXrank/stylesheets/index.css" rel="stylesheet"/>
  <script async="" defer="" src="https://buttons.github.io/buttons.js"></script>
  <script src="/ReXrank/javascripts/analytics.js"></script>
  <!-- 引入 jQuery 和 tablesorter 插件 -->
  <script src="/ReXrank/bower_components/jquery/dist/jquery.min.js"></script>
  <script src="/ReXrank/javascripts/jquery.tablesorter.min.js"></script>
  <link rel="stylesheet" href="/ReXrank/stylesheets/theme.default.min.css">
  <style>
    .fixed-height-table {
      height: 430px; /* 固定高度，可根据需要调整 */
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
              <a href="/ReXrank/">Home</a>
            </li>
          </ul>
        </div>
      </div>
      <div class="leftNav">
        <div class="brandDiv">
          <a class="navbar-brand" href="/ReXrank/">ReXrank</a>
        </div>
      </div>
    </div>
  </div>
  <div class="cover" id="topCover">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h1 id="appTitle">ReXrank</h1>
          <h2 id="appSubtitle">Open-Source Radiology Report Generation Leaderboard</h2>
        </div>
      </div>
    </div>
  </div>
  <div class="cover" id="contentCover">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <div class="infoCard">
            <div class="infoBody">
              <div class="infoHeadline">
                <h2>What is ReXrank?</h2>
              </div>
              <p>
              <b>ReXrank</b> is an open-source leaderboard for AI-powered radiology report generation from chest x-ray images. We're setting a new standard in healthcare AI by providing a comprehensive, objective evaluation framework for cutting-edge models. Our mission is to accelerate progress in this critical field by fostering healthy competition and collaboration among researchers, clinicians, and AI enthusiasts.
                Using diverse datasets like MIMIC-CXR, IU-Xray, and CheXpert Plus, ReXrank offers a robust benchmarking system that evolves with clinical needs and technological advancements. Our leaderboard showcases top-performing models, driving innovation that could transform patient care and streamline medical workflows. </p>
               <p> Join us in shaping the future of AI-assisted radiology. Develop your models, submit your results, and see how you stack up against the best in the field. Together, we can push the boundaries of what's possible in medical imaging and report generation. </p>
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-5">
          <div class="infoCard">
            <div class="infoBody">
              <div class="infoHeadline">
                <h2>Getting Started</h2>
              </div>
              <p>
                To evaluate your models, we made available the evaluation script we will use for official evaluation, along with a sample prediction file that the script will take as input.
                To run the evaluation, use
                <code>
                  python evaluate.py &lt;path_to_data&gt; &lt;path_to_predictions&gt;
                </code>.
              </p>
              <ul class="list-unstyled">
                <li>
                  <a class="btn actionBtn inverseBtn" download="" href="https://github.com/xiaoman-zhang/ReXrank/blob/gh-pages/example_files/evaluation_script.md" target="_blank">Evaluation Script</a>
                </li>                
                <li>
                  <a class="btn actionBtn inverseBtn" download="" href="https://github.com/xiaoman-zhang/ReXrank/blob/gh-pages/example_files/prediction.json" target="_blank">Sample Prediction File</a>
                </li>
              </ul>
              <p>
                Once you have a built a model that works to your expectations on the MIMIC-CXR test set, you submit it to get official scores on our Private test set. Here's a tutorial on the submission for a smooth evaluation process.
              </p>
              <a class="btn actionBtn inverseBtn" href="https://github.com/xiaoman-zhang/ReXrank/blob/gh-pages/example_files/submission_tutorial.md" target="_blank">Submission Tutorial</a>
              <p>
                Please <b><a href="https://github.com/xiaoman-zhang/ReXrank/blob/gh-pages/cite.txt" target="_blank">cite</a> </b>if you find our leaderboard helpful. </p>
              <p> To keep up to date with major changes to the leaderboard and dataset, please <b><a href="https://forms.gle/bZpsPUccYF1Th7Xv9" target="_blank">subscribe</a></b> here ! 
              </p>
              <!-- <div id="mc_embed_signup">
                <form action="//google.us13.list-manage.com/subscribe/post?u=1842e6560d6e10316b4e1aaf5&amp;id=76586bdcf4" class="validate" id="mc-embedded-subscribe-form" method="post" name="mc-embedded-subscribe-form" novalidate="" target="_blank">
                  <div id="mc_embed_signup_scroll">
                    <input class="email" id="mce-EMAIL" name="EMAIL" placeholder="email address" required="" type="email" value=""/>
                    <div aria-hidden="true" style="position: absolute; left: -5000px;">
                      <input name="b_1842e6560d6e10316b4e1aaf5_76586bdcf4" tabindex="-1" type="text" value=""/>
                    </div>
                    <div class="clear">
                      <input class="button" id="mc-embedded-subscribe" name="subscribe" type="submit" value="Subscribe"/>
                    </div>
                  </div>
                </form>
              </div> -->
            </div>
          </div>
        </div>'''
    mid_html = '''{table_rank_html} {table_mimiccxr_html} {table_iuxray_html} {table_chexpertplus_html} '''.format(table_chexpertplus_html=table_chexpertplus_html, table_iuxray_html=table_iuxray_html, table_mimiccxr_html=table_mimiccxr_html, table_rank_html=table_rank_html)
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
                sortList: [[2, 0]] // Default sort by RadCliQ-v1 ascending
            });
    
            // Update ranks after sorting
            function updateRankTest() {
                $("#modelTableTest tbody:visible tr").each(function(index) {
                    $(this).find("td:eq(0) p").text(index + 1);
                });
            }
            
            // Function to sort table based on custom order for clicked column
            function customSortTest(columnIndex) {
                var sortOrder = [0, 0, 1, 1, 1, 1]; // 示例排序顺序数组
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
            $("#modelTableValid").tablesorter({
                theme: 'default',
                headers: {
                    0: { sorter: false }, // Rank column
                    1: { sorter: false }  // Model column
                },
                sortList: [[2, 0]] // Default sort by RadCliQ-v1 ascending
            });
    
            // Update ranks after sorting
            function updateRankValid() {
                $("#modelTableValid tbody:visible tr").each(function(index) {
                    $(this).find("td:eq(0) p").text(index + 1);
                });
            }
            
            // Function to sort table based on custom order for clicked column
            function customSortValid(columnIndex) {
                var sortOrder = [0, 0, 1, 1, 1, 1]; // 示例排序顺序数组
                var sortDirection = sortOrder[columnIndex - 2]; // 获取点击列对应的排序方向
                $("#modelTableValid").trigger("sorton", [[[columnIndex, sortDirection]]]);
            }

            // Detect column header click and apply custom sort
            $("#modelTableValid th").click(function() {
                var columnIndex = $(this).index();
                if (columnIndex > 1) { // 只对第2列及之后的列进行排序
                  customSortValid(columnIndex);
                }
            });
            // Update ranks after table sort ends
            $("#modelTableValid").bind("sortEnd", function() {
              updateRankValid();
            });

            // Initialize tablesorter
            $("#modelTableIU").tablesorter({
                theme: 'default',
                headers: {
                    0: { sorter: false }, // Rank column
                    1: { sorter: false }  // Model column
                },
                sortList: [[2, 0]] // Default sort by RadCliQ-v1 ascending
            });
    
            // Update ranks after sorting
            function updateRanksIU() {
                $("#modelTableIU tbody:visible tr").each(function(index) {
                    $(this).find("td:eq(0) p").text(index + 1);
                });
            }

            // Function to sort table based on custom order for clicked column
            function customSortIU(columnIndex) {
                var sortOrder = [0, 0, 1, 1, 1, 1]; // 示例排序顺序数组
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
    
            $("#modelTableValid").hide();
            // Update ranks on page load
            updateRanksIU();
            
            // Initialize tablesorter
            $("#modelTableCheXpert").tablesorter({
                theme: 'default',
                headers: {
                    0: { sorter: false }, // Rank column
                    1: { sorter: false }  // Model column
                },
                sortList: [[2, 0]] // Default sort by RadCliQ-v1 ascending
            });
    
            // Update ranks after sorting
            function updateRanksCheXpert() {
                $("#modelTableCheXpert tbody:visible tr").each(function(index) {
                    $(this).find("td:eq(0) p").text(index + 1);
                });
            }
    
            // Function to sort table based on custom order for clicked column
            function customSortCheXpert(columnIndex) {
                var sortOrder = [0, 0, 1, 1, 1, 1]; // 示例排序顺序数组
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

            // Switch to test results
            $("#testBtn").click(function() {
                $("#modelTableTest").show();
                $("#modelTableValid").hide();
                $(this).removeClass('btn-gray').addClass('btn-black');
                $("#validBtn").removeClass('btn-black').addClass('btn-gray');
                updateRanksTest(); // Update ranks after switching
            });

            // Switch to valid results
            $("#validBtn").click(function() {
                $("#modelTableTest").hide();
                $("#modelTableValid").show();
                $(this).removeClass('btn-gray').addClass('btn-black');
                $("#testBtn").removeClass('btn-black').addClass('btn-gray');
                updateRanksValid(); // Update ranks after switching
            });

            // Switch to test results
            $("#testBtnIU").click(function() {
                $("#testResultsIU").show();
                $("#validResultsIU").hide();
                $(this).removeClass('btn-gray').addClass('btn-black');
                $("#validBtnIU").removeClass('btn-black').addClass('btn-gray');
                updateRanksIU(); // Update ranks after switching
            });
    
            // Switch to valid results
            $("#validBtnIU").click(function() {
                $("#testResultsIU").hide();
                $("#validResultsIU").show();
                $(this).removeClass('btn-gray').addClass('btn-black');
                $("#testBtnIU").removeClass('btn-black').addClass('btn-gray');
                updateRanksIU(); // Update ranks after switching
            });
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
table_rank_html = './results/table_rank.html'

generate_html(get_html_content(table_chexpertplus_html), get_html_content(table_iuxray_html), get_html_content(table_mimiccxr_html), get_html_content(table_rank_html),save_html_path='./index.html')