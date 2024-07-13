import pandas as pd

def generate_leaderboard_html(mimic_csv_path, private_csv_path, output_path):
    # 读取两个CSV文件
    df_mimic = pd.read_csv(mimic_csv_path)
    df_private = pd.read_csv(private_csv_path)
    
    # 根据RadCliQ-v1分数进行排序
    df_mimic = df_mimic.sort_values(by='RadCliQ-v1', ascending=True).reset_index(drop=True)
    df_private = df_private.sort_values(by='RadCliQ-v1', ascending=True).reset_index(drop=True)
    
    # HTML开头部分
    html_string = '''
    <div class="col-md-7">
      <div class="infoCard">
        <div class="infoBody">
          <div class="infoHeadline">
            <h2>Leaderboard Overview</h2>
          </div>
          <p>Include top models for different datasets.</p>
          <div class="fixed-height-table">
            <table class="table performanceTable">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>MIMIC-CXR</th>
                  <th>Private Dataset</th>
                </tr>
              </thead>
              <tbody>
    '''
    
    # 获取最长的排名数
    max_rank = max(len(df_mimic), len(df_private))
    
    # 生成表格内容
    for i in range(max_rank):
        html_string += '<tr>'
        
        html_string += f'<td><p>{i+1}</p></td>'
        
        if i < len(df_mimic):
            row_mimic = df_mimic.iloc[i]
            html_string += f'''
            <td style="word-break:break-word;">
              <a class="link" href="{row_mimic['Model URL']}">{row_mimic['Model Name']}</a>
              <p class="institution">{row_mimic['Institution']}</p>
            </td>
            '''
        else:
            html_string += '<td style="word-break:break-word;"></td>'
        
        if i < len(df_private):
            row_private = df_private.iloc[i]
            html_string += f'''
            <td style="word-break:break-word;">
              <a class="link" href="{row_private['Model URL']}">{row_private['Model Name']}</a>
              <p class="institution">{row_private['Institution']}</p>
            </td>
            '''
        else:
            html_string += '<td style="word-break:break-word;"></td>'
        
        html_string += '</tr>'
    
    # HTML结尾部分
    html_string += '''
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    '''
    
    # 写入HTML文件
    with open(output_path, 'w') as file:
        file.write(html_string)


# 调用函数生成HTML文件
generate_leaderboard_html('./results/result_mimiccxr.csv', './results/result_mimiccxr.csv', './results/table_rank.html')
