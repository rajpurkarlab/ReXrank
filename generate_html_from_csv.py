import pandas as pd



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
                <h2>ReXrank Challenge V1.0 - RRG Performance on MIMIC-CXR</h2>
              </div>
              <div><p> <a class="link" href="https://physionet.org/content/mimic-cxr/2.0.0/">MIMIC-CXR </a> contains 377,110 images corresponding to 227,835 radiographic studies performed at the Beth Israel Deaconess Medical Center in Boston, MA. We follow the official split of MIMIC-CXR in the following experiments.</p>
              </div>
              <div>
                <button id="testBtnMIMIC" class="btn btn-black">Findings</button>
                <button id="validBtnMIMIC" class="btn btn-gray">Findings + Impression</button>
              </div>
              <table class="table performanceTable tablesorter" id="modelTableTest">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Model</th>
                    <th>1/RadCliQ-v1</th>
                    <th>BLEU</th>
                    <th>BertScore</th>
                    <th>SembScore</th>
                    <th>RadGraph</th>
                    <th>RaTEScore</th>
                    <th>GREEN</th>
                  </tr>
                </thead>
                <tbody id="testResultsMIMIC">
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
                <td><b>{row['1/RadCliQ-v1']}</b></td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RaTEScore']}</b></td>
                <td><b>{row['GREEN']}</b></td>
              </tr>
        '''
    
    html_string += '''
            </tbody>
            <tbody id="validResultsMIMIC" style="display: none;">
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
               <td><b>{row['1/RadCliQ-v1']}</b></td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RaTEScore']}</b></td>
                <td><b>{row['GREEN']}</b></td>
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


def generate_leaderboard_html_gradienthealth(test_csv_path, valid_csv_path, output_path):
    # 读取CSV文件
    df_test = pd.read_csv(test_csv_path)
    df_valid = pd.read_csv(valid_csv_path)
    
    
    # HTML开头部分
    html_string = '''
    <div class="col-md-12">
    <div class="infoCard">
      <div class="infoBody">
        <div class="infoHeadline">
          <h2>ReXrank Challenge V1.0 - RRG Performance on ReXGradient</h2>
        </div>
        <div>
          <p> ReXGradient is a large-scale private test dataset contains 10,000 studies collected from different medical centers in the US. </p>
        </div>
        <div style="margin-top: 5px;">
          <button id="testBtnPrivate" class="btn btn-black">Findings</button>
          <button id="validBtnPrivate" class="btn btn-gray">Findings + Impression</button>
        </div>
        <table class="table performanceTable tablesorter" id="modelTablePrivate">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Model</th>
              <th>1/RadCliQ-v1</th>
              <th>BLEU</th>
              <th>BertScore</th>
              <th>SembScore</th>
              <th>RadGraph</th>
              <th>RaTEScore</th>
              <th>GREEN</th>
            </tr>
          </thead>
          <tbody id="testResultsPrivate">
    '''
    
    # 生成表格内容
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
                <td><b>{row['1/RadCliQ-v1']}</b></td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RaTEScore']}</b></td>
                <td><b>{row['GREEN']}</b></td>
              </tr>
        '''
    
    html_string += '''
            </tbody>
            <tbody id="validResultsPrivate" style="display: none;">
    '''

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
                <td><b>{row['1/RadCliQ-v1']}</b></td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RaTEScore']}</b></td>
                <td><b>{row['GREEN']}</b></td>
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



def generate_leaderboard_html_chexpertplus(test_csv_path, valid_csv_path, output_path):
    # 读取CSV文件
    df_test = pd.read_csv(test_csv_path)
    df_valid = pd.read_csv(valid_csv_path)
    
    
    # HTML开头部分
    html_string = '''
    <div class="col-md-12">
    <div class="infoCard">
      <div class="infoBody">
        <div class="infoHeadline">
          <h2>ReXrank Challenge V1.0 - RRG Performance on CheXpert Plus</h2>
        </div>
        <div>
          <p> <a class="link" href="https://stanfordaimi.azurewebsites.net/datasets/5158c524-d3ab-4e02-96e9-6ee9efc110a1">CheXpert Plus </a> contains 223,228 unique pairs of radiology reports and chest X-rays from 187,711 studies and 64,725 patients. We follow the official split of CheXpert Plus in the following experiments and use the valid set for evaluation.</p>
        </div>
        <div style="margin-top: 5px;">
          <button id="testBtnCheXpert" class="btn btn-black">Findings</button>
          <button id="validBtnCheXpert" class="btn btn-gray">Findings + Impression</button>
        </div>
        <table class="table performanceTable tablesorter" id="modelTableCheXpert">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Model</th>
              <th>1/RadCliQ-v1</th>
              <th>BLEU</th>
              <th>BertScore</th>
              <th>SembScore</th>
              <th>RadGraph</th>
              <th>RaTEScore</th>
              <th>GREEN</th>
            </tr>
          </thead>
          <tbody id="testResultsCheXpert">
    '''
    
    # 生成表格内容
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
                <td><b>{row['1/RadCliQ-v1']}</b></td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RaTEScore']}</b></td>
                <td><b>{row['GREEN']}</b></td>
              </tr>
        '''
    html_string += '''
            </tbody>
            <tbody id="validResultsCheXpert" style="display: none;">
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
                <td><b>{row['1/RadCliQ-v1']}</b></td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RaTEScore']}</b></td>
                <td><b>{row['GREEN']}</b></td>
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
            <h2>ReXrank Challenge V1.0 - RRG Performance on IU Xray</h2>
          </div>
          <div>
            <p> <a class="link" href="https://paperswithcode.com/dataset/iu-x-ray">IU Xray</a> contains 7,470 pairs of radiology reports and chest X-rays from Indiana University. We follow the split given by <a class="link" href="https://github.com/cuhksz-nlp/R2Gen">R2Gen</a>.</p>
          </div>
          <div style="margin-top: 5px;">
            <button id="testBtnIU" class="btn btn-black">Findings</button>
            <button id="validBtnIU" class="btn btn-gray">Findings + Impression</button>
          </div>
          <table class="table performanceTable tablesorter" id="modelTableIU">
            <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Model</th>
                    <th>1/RadCliQ-v1</th>
                    <th>BLEU</th>
                    <th>BertScore</th>
                    <th>SembScore</th>
                    <th>RadGraph</th>
                    <th>RaTEScore</th>
                    <th>GREEN</th>
                  </tr>
                </thead>
            <tbody id="testResultsIU">
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
                <td><b>{row['1/RadCliQ-v1']}</b></td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RaTEScore']}</b></td>
                <td><b>{row['GREEN']}</b></td>
              </tr>
        '''
    
    html_string += '''
            </tbody>
            <tbody id="validResultsIU" style="display: none;">
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
                <td><b>{row['1/RadCliQ-v1']}</b></td>
                <td><b>{row['BLEU']}</b></td>
                <td><b>{row['BertScore']}</b></td>
                <td><b>{row['SembScore']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RaTEScore']}</b></td>
                <td><b>{row['GREEN']}</b></td>
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



generate_leaderboard_html_iu_xray('./results/findings_result_iu_xray.csv','./results/result_iu_xray.csv','./results/table_iuxray.html')
generate_leaderboard_html_chexpertplus('./results/findings_result_chexpertplus.csv','./results/result_chexpertplus.csv','./results/table_chexpertplus.html')
generate_leaderboard_html_gradienthealth('./results/findings_result_gradienthealth.csv','./results/result_gradienthealth.csv','./results/table_gradienthealth.html')
generate_leaderboard_html_mimiccxr('./results/findings_result_mimiccxr.csv','./results/result_mimiccxr.csv','./results/table_mimiccxr.html')
