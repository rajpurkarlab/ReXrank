import pandas as pd



import pandas as pd



def generate_html_from_csv(csv_path, output_path):
    # Read CSV file
    df = pd.read_csv(csv_path)
    
    # HTML header
    html_string = '''
    <div class="col-md-12">
    <div class="infoCard">
      <div class="infoBody">
        <div class="infoHeadline">
          <h2>ReXrank Challenge V2.0 - VQA Performance on ReXVQA</h2>
        </div>
        <div>
          <p>Performance comparison of various vision-language models on medical VQA tasks. </p>
        </div>
        <table class="table performanceTable tablesorter" id="modelTableVQA">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Model</th>
              <th>Overall Accuracy </th>
              <th>Differential Diagnosis </th>
              <th>Geometric Information </th>
              <th>Location Assessment </th>
              <th>Negation Assessment </th>
              <th>Presence Assessment </th>
            </tr>
          </thead>
          <tbody>
    '''
    
    # Generate table content
    for _, row in df.iterrows():
        html_string += f'''
              <tr>
                <td>{row['Rank']}</td>
                <td style="word-break:break-word;">
                  <a class="link" href="{row['Model URL']}">{row['Model Name']}</a>
                  <p class="institution">{row['Institution']}</p>
                </td>
                <td><b>{row['Overall Accuracy']:.4f}</b></td>
                <td><b>{row['Differential Diagnosis']:.4f}</b></td>
                <td><b>{row['Geometric Information Assessment']:.4f}</b></td>
                <td><b>{row['Location and Distribution Assessment']:.4f}</b></td>
                <td><b>{row['Negation Assessment']:.4f}</b></td>
                <td><b>{row['Presence Assessment']:.4f}</b></td>
              </tr>
        '''
    
    # HTML footer
    html_string += '''
            </tbody>
          </table>
        </div>
      </div>
    </div>
    '''
    
    # Write HTML file
    with open(output_path, 'w') as file:
        file.write(html_string)



# 调用函数生成HTML文件
generate_html_from_csv('./vqa_results/vqa_results.csv', './vqa_results/vqa_results.html')
