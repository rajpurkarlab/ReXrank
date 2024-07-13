import pandas as pd



def generate_html_from_csv(csv_path, output_path):
    # 读取CSV文件
    df = pd.read_csv(csv_path)
    
    # HTML开头部分
    html_string = '''
    <div class="col-md-12">
      <div class="infoCard">
        <div class="infoBody">
          <div class="infoHeadline">
            <h2>Leaderboard on MIMIC-CXR Dataset</h2>
          </div>
          <p>Info about the dataset.</p>
          <table class="table performanceTable tablesorter" id="modelTable">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Model</th>
                <th>BLEU</th>
                <th>Bert-Sim</th>
                <th>RadGraph</th>
                <th>RadCliQ-v1</th>
                <th>KG-Sim</th>
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
                <td><b>{row['Bert-Sim']}</b></td>
                <td><b>{row['RadGraph']}</b></td>
                <td><b>{row['RadCliQ-v1']}</b></td>
                <td><b>{row['KG-Sim']}</b></td>
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


import pandas as pd

# Data to create DataFrame
data = {
    "Rank": [1, 2, 3, 4, 5, 6, 7, 8],
    "Date": ["2024-07-13"] * 8,
    "Model Name": ["CheXpertPlus-Baseline", "MedVersa", "LLM-CXR", "CheXagent", "RadFM", "VLCI", "CvT2DistilGPT2", "RGRG"],
    "Institution": ["Institution1", "Institution2", "Institution3", "Institution4", "Institution5", "Institution6", "Institution7", "Institution8"],
    "Model URL": [
        "https://example.com/model1", 
        "https://example.com/model2", 
        "https://example.com/model3", 
        "https://example.com/model4", 
        "https://example.com/model5", 
        "https://example.com/model6", 
        "https://example.com/model7", 
        "https://example.com/model8"
    ],
    "BLEU": [90.939, 91.939, 89.939, 88.939, 87.939, 86.939, 85.939, 84.939],
    "Bert-Sim": [93.214, 94.214, 92.214, 91.214, 90.214, 89.214, 88.214, 87.214],
    "RadGraph": [93.214, 94.214, 92.214, 91.214, 90.214, 89.214, 88.214, 87.214],
    "RadCliQ-v1": [93.214, 94.214, 92.214, 91.214, 90.214, 89.214, 88.214, 87.214],
    "KG-Sim": [93.214, 94.214, 92.214, 91.214, 90.214, 89.214, 88.214, 87.214]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv('./results/result_mimiccxr.csv', index=False)

# 调用函数生成HTML文件
generate_html_from_csv('./results/result_mimiccxr.csv', './results/table_mimiccxr.html')

