import pandas as pd

def generate_leaderboard_html_v2(rexvqa_csv_path, output_path):
    df_rexvqa = pd.read_csv(rexvqa_csv_path)
    
    # Sort each dataframe by their respective metrics
    df_rexvqa = df_rexvqa.sort_values(by='Overall Accuracy', ascending=False).reset_index(drop=True)
    
    # HTML header
    html_string = '''
    <div class="col-md-7 right-column">
      <div class="infoCard">
        <div class="infoBody">
          <div class="infoHeadline">
            <h2>ReXrank Challenge V2.0 Leaderboard (VQA)</h2>
          </div>
          <div class="fixed-height-table">
            <table class="table performanceTable">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>ReXVQA</th>
                </tr>
              </thead>
              <tbody>
    '''

    # Get the maximum rank length
    max_rank = len(df_rexvqa)
    
    # Generate table content
    for i in range(max_rank):
        html_string += '<tr>'

        html_string += f'<td><p>{i+1}</p></td>'
        
        row_rexvqa = df_rexvqa.iloc[i]
        html_string += f'''
        <td style="word-break:break-word;">
          <a class="link" href="{row_rexvqa['Model URL']}">{row_rexvqa['Model Name']}</a>
          <p class="institution">{row_rexvqa['Institution']}</p>
        </td>
        '''
        
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



def generate_leaderboard_html_v1(private_csv_path, mimic_csv_path, iu_xray_csv_path, chexpert_plus_csv_path, output_path):
    # Read the CSV files
    df_mimic = pd.read_csv(mimic_csv_path)
    df_iu_xray = pd.read_csv(iu_xray_csv_path)
    df_chexpert_plus = pd.read_csv(chexpert_plus_csv_path)
    df_private = pd.read_csv(private_csv_path)
    
    # Sort each dataframe by their respective metrics
    df_private = df_private.sort_values(by='1/FineRadScore', ascending=False).reset_index(drop=True)
    df_mimic = df_mimic.sort_values(by='1/FineRadScore', ascending=False).reset_index(drop=True)
    df_iu_xray = df_iu_xray.sort_values(by='1/FineRadScore', ascending=False).reset_index(drop=True)
    df_chexpert_plus = df_chexpert_plus.sort_values(by='1/FineRadScore', ascending=False).reset_index(drop=True)
    
    # HTML header
    html_string = '''
    <div class="col-md-7 right-column">
      <div class="infoCard">
        <div class="infoBody">
          <div class="infoHeadline">
            <h2>ReXrank Challenge V1.0 Leaderboard (RRG)</h2>
          </div>
          <div class="fixed-height-table">
            <table class="table performanceTable">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>ReXGradient</th>
                  <th>MIMIC-CXR</th>
                  <th>IU-Xray</th>
                  <th>CheXpert Plus</th>
                </tr>
              </thead>
              <tbody>
    '''

    # Get the maximum rank length
    max_rank = max(len(df_private), len(df_mimic), len(df_iu_xray), len(df_chexpert_plus))
    
    # Generate table content
    for i in range(max_rank):
        html_string += '<tr>'
        
        html_string += f'<td><p>{i+1}</p></td>'
        
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


def generate_leaderboard_html(private_csv_path, mimic_csv_path, iu_xray_csv_path, chexpert_plus_csv_path, rexvqa_csv_path, output_path):
    # Read the CSV files
    df_mimic = pd.read_csv(mimic_csv_path)
    df_iu_xray = pd.read_csv(iu_xray_csv_path)
    df_chexpert_plus = pd.read_csv(chexpert_plus_csv_path)
    df_private = pd.read_csv(private_csv_path)
    df_rexvqa = pd.read_csv(rexvqa_csv_path)
    
    # Sort each dataframe by their respective metrics
    df_private = df_private.sort_values(by='1/FineRadScore', ascending=False).reset_index(drop=True)
    df_mimic = df_mimic.sort_values(by='1/FineRadScore', ascending=False).reset_index(drop=True)
    df_iu_xray = df_iu_xray.sort_values(by='1/FineRadScore', ascending=False).reset_index(drop=True)
    df_chexpert_plus = df_chexpert_plus.sort_values(by='1/FineRadScore', ascending=False).reset_index(drop=True)
    df_rexvqa = df_rexvqa.sort_values(by='Overall Accuracy', ascending=False).reset_index(drop=True)

    # HTML header
    html_string = '''
    <div class="col-md-12">
      <div class="infoCard">
        <div class="infoBody">
          <div class="infoHeadline">
            <h2>Leaderboard Overview</h2>
          </div>
          <p>Include top models for different datasets. * denotes model trained on this dataset.</p>
          <div class="fixed-height-table">
            <table class="table performanceTable">
              <thead>
                <tr>
                  <th rowspan="2">Rank</th>
                  <th colspan="4">Report Generation</th>
                  <th>VQA</th>
                </tr>
                <tr>
                  <th>ReXGradient</th>
                  <th>MIMIC-CXR</th>
                  <th>IU-Xray</th>
                  <th>CheXpert Plus</th>
                  <th>ReXVQA</th>
                </tr>
              </thead>
              <tbody>
    '''
    
    # Get the maximum rank length
    max_rank = max(len(df_private), len(df_mimic), len(df_iu_xray), len(df_chexpert_plus), len(df_rexvqa))
    
    # Generate table content
    for i in range(max_rank):
        html_string += '<tr>'
        
        html_string += f'<td><p>{i+1}</p></td>'
        
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
        
        if i < len(df_rexvqa):
            row_rexvqa = df_rexvqa.iloc[i]
            html_string += f'''
            <td style="word-break:break-word;">
              <a class="link" href="{row_rexvqa['Model URL']}">{row_rexvqa['Model Name']}</a>
              <p class="institution">{row_rexvqa['Institution']}</p>
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
# generate_leaderboard_html('./results/findings_result_gradienthealth.csv','./results/findings_result_mimiccxr.csv', './results/findings_result_iu_xray.csv', './results/findings_result_chexpertplus.csv', './vqa_results/vqa_results.csv', './results/table_rank.html')

generate_leaderboard_html_v1('./results/findings_result_gradienthealth.csv','./results/findings_result_mimiccxr.csv', './results/findings_result_iu_xray.csv', './results/findings_result_chexpertplus.csv', './results/table_rank_v1.html')
generate_leaderboard_html_v2('./vqa_results/vqa_results.csv', './results/table_rank_v2.html')