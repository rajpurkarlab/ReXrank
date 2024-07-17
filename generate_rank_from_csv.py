import pandas as pd

def generate_leaderboard_html(mimic_csv_path, iu_xray_csv_path, chexpert_plus_csv_path, output_path):
    # Read the three CSV files
    df_mimic = pd.read_csv(mimic_csv_path)
    df_iu_xray = pd.read_csv(iu_xray_csv_path)
    df_chexpert_plus = pd.read_csv(chexpert_plus_csv_path)
    
    # Sort each dataframe by 'RadCliQ-v1' score in ascending order
    df_mimic = df_mimic.sort_values(by='RadCliQ-v1', ascending=True).reset_index(drop=True)
    df_iu_xray = df_iu_xray.sort_values(by='RadCliQ-v1', ascending=True).reset_index(drop=True)
    df_chexpert_plus = df_chexpert_plus.sort_values(by='RadCliQ-v1', ascending=True).reset_index(drop=True)
    
    # HTML header
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
                  <th>IU-Xray</th>
                  <th>CheXpert Plus</th>
                </tr>
              </thead>
              <tbody>
    '''
    
    # Get the maximum rank length
    max_rank = max(len(df_mimic), len(df_iu_xray), len(df_chexpert_plus))
    
    # Generate table content
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
        
        if i < len(df_iu_xray):
            row_iu_xray = df_iu_xray.iloc[i]
            html_string += f'''
            <td style="word-break:break-word;">
              <a class="link" href="{row_iu_xray['Model URL']}">{row_iu_xray['Model Name']}</a>
              <p class="institution">{row_iu_xray['Institution']}</p>
            </td>
            '''
        else:
            html_string += '<td style="word-break:break-word;"></td>'
        
        if i < len(df_chexpert_plus):
            row_chexpert_plus = df_chexpert_plus.iloc[i]
            html_string += f'''
            <td style="word-break:break-word;">
              <a class="link" href="{row_chexpert_plus['Model URL']}">{row_chexpert_plus['Model Name']}</a>
              <p class="institution">{row_chexpert_plus['Institution']}</p>
            </td>
            '''
        else:
            html_string += '<td style="word-break:break-word;"></td>'
        
        html_string += '</tr>'
    
    # HTML footer
    html_string += '''
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    '''
    
    # Write the HTML content to the output file
    with open(output_path, 'w') as file:
        file.write(html_string)


# Call the function to generate the HTML file
generate_leaderboard_html('./results/result_mimiccxr.csv', './results/result_mimiccxr.csv', './results/result_mimiccxr.csv', './results/table_rank.html')

# # 调用函数生成HTML文件
# generate_leaderboard_html('./results/result_mimiccxr.csv', './results/result_mimiccxr.csv', './results/table_rank.html')
