import pandas as pd



def generate_html_from_csv_chexpertplus(csv_path, output_path):
    # 读取CSV文件
    df = pd.read_csv(csv_path)
    
    # HTML开头部分
    html_string = '''
    <div class="col-md-12">
          <div class="infoCard">
            <div class="infoBody">
              <div class="infoHeadline">
                <h2>Leaderboard on CheXpert Plus Dataset</h2>
              </div>
              <div> <p> CheXpert Plus is a dataset that pairs text and images, featuring 223,228 unique pairs of radiology reports and chest X-rays from 187,711 studies and 64,725 patients. We follow the official split of CheXpert Plus in the following experiments, and use the valid set for evaluation.</p> </div>
              <table class="table performanceTable tablesorter" id="modelTableCheXpert">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Model</th>
                    <th>BLEU</th>
                    <th>BertScore</th>
                    <th>SembScore</th>
                    <th>RadGraph</th>
                    <th>RadCliQ-v0</th>
                    <th>RadCliQ-v1</th>
                  </tr>
                </thead>
                <tbody>
    '''
    
    # 生成表格内容
    for _, row in df.iterrows():
        html_string += f'''
              <tr>
                <td>
                  <p>{row['Rank']}</p>
                  <span class="date label label-default">{row['Date']}</span>
                </td>
                <td style="word-break:break-word;">
                  <a class="link" href="{row['Model URL']}">{row['Model Name']}</a>
                  <p class="institution">{row['Institution']}</p>
                </td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RadCliQ-v0']}</b></td>
                <td><b>{row['RadCliQ-v1']}</b></td>
              </tr>
        '''
    
    # HTML结尾部分
    html_string += '''
            </tbody>
          </table>
        </div>
      </div>
    </div>
    '''
    
    # 写入HTML文件
    with open(output_path, 'w') as file:
        file.write(html_string)



def generate_leaderboard_html_mimiccxr(test_csv_path, valid_csv_path, output_path):
    # 读取CSV文件
    df_test = pd.read_csv(test_csv_path)
    df_valid = pd.read_csv(valid_csv_path)
    
    # HTML开头部分
    html_string = '''
    <div class="col-md-12">
          <div class="infoCard">
            <div class="infoBody">
              <div class="infoHeadline">
                <h2>Leaderboard on MIMIC-CXR Dataset</h2>
              </div>
              <div> <p>MIMIC-CXR contains 377,110 images corresponding to 227,835 radiographic studies performed at the Beth Israel Deaconess Medical Center in Boston, MA. We follow the official split of MIMIC-CXR in the following experiments.</p> </div>
              <div>
                <button id="MIMICTestBtn" class="btn btn-black">MIMIC-CXR Test</button>
                <button id="MIMICValidBtn" class="btn btn-gray">MIMIC-CXR Valid</button>
              </div>
              <table class="table performanceTable tablesorter" id="modelTableMIMIC">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Model</th>
                    <th>BLEU</th>
                    <th>BertScore</th>
                    <th>SembScore</th>
                    <th>RadGraph</th>
                    <th>RadCliQ-v0</th>
                    <th>RadCliQ-v1</th>
                  </tr>
                </thead>
                <tbody id="testResults">
    '''
    
    # 生成测试集表格内容
    for _, row in df_test.iterrows():
        html_string += f'''
              <tr>
                <td>
                  <p>{row['Rank']}</p>
                  <span class="date label label-default">{row['Date']}</span>
                </td>
                <td style="word-break:break-word;">
                  <a class="link" href="{row['Model URL']}">{row['Model Name']}</a>
                  <p class="institution">{row['Institution']}</p>
                </td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RadCliQ-v0']}</b></td>
                <td><b>{row['RadCliQ-v1']}</b></td>
              </tr>
        '''
    
    html_string += '''
            </tbody>
            <tbody id="validResults" style="display: none;">
    '''
    
    # 生成验证集表格内容
    for _, row in df_valid.iterrows():
        html_string += f'''
              <tr>
                <td>
                  <p>{row['Rank']}</p>
                  <span class="date label label-default">{row['Date']}</span>
                </td>
                <td style="word-break:break-word;">
                  <a class="link" href="{row['Model URL']}">{row['Model Name']}</a>
                  <p class="institution">{row['Institution']}</p>
                </td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RadCliQ-v0']}</b></td>
                <td><b>{row['RadCliQ-v1']}</b></td>
              </tr>
        '''
    
    # HTML结尾部分
    html_string += '''
            </tbody>
          </table>
        </div>
      </div>
    </div>
    '''
    
    # 写入HTML文件
    with open(output_path, 'w') as file:
        file.write(html_string)

def generate_leaderboard_html_iu_xray(test_csv_path, valid_csv_path, output_path):
    # 读取CSV文件
    df_test = pd.read_csv(test_csv_path)
    df_valid = pd.read_csv(valid_csv_path)
    
    # HTML开头部分
    html_string = '''
    <div class="col-md-12">
          <div class="infoCard">
            <div class="infoBody">
               <div class="infoHeadline">
                <h2>Leaderboard on IU Xray Dataset</h2>
              </div>
              <div> <p>IU Xray is s a set of chest X-ray images paired with their corresponding diagnostic reports. The dataset contains 7,470 pairs of images and reports. We follow the split given by <a class="link" href="https://github.com/cuhksz-nlp/R2Gen">R2Gen</a> </p> </div>
              <div>
                <button id="IUTestBtn" class="btn btn-black">IU Xray Test</button>
                <button id="IUValidBtn" class="btn btn-gray">IU Xray Valid</button>
            </div>
            <table class="table performanceTable tablesorter" id="modelTableIU">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Model</th>
                    <th>BLEU</th>
                    <th>BertScore</th>
                    <th>SembScore</th>
                    <th>RadGraph</th>
                    <th>RadCliQ-v0</th>
                    <th>RadCliQ-v1</th>
                  </tr>
                </thead>
                <tbody id="testResults">
    '''
    
    # 生成测试集表格内容
    for _, row in df_test.iterrows():
        html_string += f'''
              <tr>
                <td>
                  <p>{row['Rank']}</p>
                  <span class="date label label-default">{row['Date']}</span>
                </td>
                <td style="word-break:break-word;">
                  <a class="link" href="{row['Model URL']}">{row['Model Name']}</a>
                  <p class="institution">{row['Institution']}</p>
                </td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RadCliQ-v0']}</b></td>
                <td><b>{row['RadCliQ-v1']}</b></td>
              </tr>
        '''
    
    html_string += '''
            </tbody>
            <tbody id="validResults" style="display: none;">
    '''
    
    # 生成验证集表格内容
    for _, row in df_valid.iterrows():
        html_string += f'''
              <tr>
                <td>
                  <p>{row['Rank']}</p>
                  <span class="date label label-default">{row['Date']}</span>
                </td>
                <td style="word-break:break-word;">
                  <a class="link" href="{row['Model URL']}">{row['Model Name']}</a>
                  <p class="institution">{row['Institution']}</p>
                </td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RadCliQ-v0']}</b></td>
                <td><b>{row['RadCliQ-v1']}</b></td>
              </tr>
        '''
    
    # HTML结尾部分
    html_string += '''
            </tbody>
          </table>
        </div>
      </div>
    </div>
    '''
    
    # 写入HTML文件
    with open(output_path, 'w') as file:
        file.write(html_string)

# 调用函数生成HTML文件
generate_html_from_csv_chexpertplus('./results/result_chexpert_plus-valid.csv', './results/table_chexpertplus.html')
generate_leaderboard_html_mimiccxr('./results/result_mimic-cxr.csv', './results/result_mimic-cxr-valid.csv', './results/table_mimiccxr.html')
generate_leaderboard_html_iu_xray('./results/result_iu_xray.csv', './results/result_iu_xray-valid.csv', './results/table_iuxray.html')


# # Data to create DataFrame
# data = {
#     "Rank": [1, 2, 3, 4, 5, 6, 7, 8],
#     "Date": ["2024-07-13"] * 8,
#     "Model Name": ["CheXpertPlus-Baseline", "MedVersa", "LLM-CXR", "CheXagent", "RadFM", "VLCI", "CvT2DistilGPT2", "RGRG"],
#     "Institution": ["Institution1", "Institution2", "Institution3", "Institution4", "Institution5", "Institution6", "Institution7", "Institution8"],
#     "Model URL": [
#         "https://example.com/model1", 
#         "https://example.com/model2", 
#         "https://example.com/model3", 
#         "https://example.com/model4", 
#         "https://example.com/model5", 
#         "https://example.com/model6", 
#         "https://example.com/model7", 
#         "https://example.com/model8"
#     ],
#     "BLEU": [90.939, 91.939, 89.939, 88.939, 87.939, 86.939, 85.939, 84.939],
#     "Bert-Sim": [93.214, 94.214, 92.214, 91.214, 90.214, 89.214, 88.214, 87.214],
#     "RadGraph": [93.214, 94.214, 92.214, 91.214, 90.214, 89.214, 88.214, 87.214],
#     "RadCliQ-v1": [93.214, 94.214, 92.214, 91.214, 90.214, 89.214, 88.214, 87.214],
#     "KG-Sim": [93.214, 94.214, 92.214, 91.214, 90.214, 89.214, 88.214, 87.214]
# }

# # Create DataFrame
# df = pd.DataFrame(data)

# # Save DataFrame to CSV
# df.to_csv('./results/result_mimiccxr.csv', index=False)

# 调用函数生成HTML文件
# generate_html_from_csv('./results/result_mimiccxr.csv', './results/table_mimiccxr.html')
