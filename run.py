import requests
from requests import post
from os.path import join, abspath
import json

api_key = ""

region = ""

project = ""

authorization_token = f"{project}:{api_key}"
header = {"Content-Type":"application/json", "Authorization": authorization_token}


def upload_pdf():
  url = "https://api-d7b62b.stack.tryrelevance.com/latest/services/get_temporary_public_file_upload_url"
  response = post(url,
                  headers=header,
                  data=json.dumps({"extension": "pdf"}))
  data = json.loads(response.text)
  return data


def upload_file_to_s3(presigned_url, file_path):
    """
    Uploads a file to an S3 bucket using a presigned URL.

    Args:
    - presigned_url: A string containing the presigned URL.
    - file_path: A string containing the path to the file to upload.

    Returns:
    A requests.Response object from the HTTP PUT request.
    """
    with open(file_path, 'rb') as file:
        files = {'file': file}
        headers = {'Content-Type': 'application/pdf','Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br, zstd',
                   'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
                   'X-Amz-Tagging': 'Expire=true'}
        response = requests.put(presigned_url, files=files, headers=headers)
    return response


def post_data(download_url, job_desc):
  url = 'https://api-d7b62b.stack.tryrelevance.com/latest/studios/66ebd849-d1eb-427f-94b2-746f66ff2d86/trigger_limited'
  response = post(url,
    headers=header,
    data=json.dumps({"params":{"job_description":job_desc,"pdf_resume":download_url},"project":"af01bd46de73-49fb-a7fc-dfeeff46b020"})
  )

  print(response)


job_description = "About the job \
\
Account Executive, Supply Chain\
\
Are you looking for a dynamic career with excellent advancement potential at a global market leader? If so, consider Gartner, the world's leading research and advisory company, serving C-suite leaders and their teams in 15,600+ distinct organizations in more than 100 countries. Gartner equips these leaders with the indispensable insights, advice, and tools to achieve their mission-critical priorities and build the successful organizations of tomorrow.\
\
Account Executives are solution-oriented individuals who help clients with their most important critical challenges. The account executive is a field sales role responsible for direct client contract value retention, as well as growth through contract expansion and the introduction of new products and services. The territory for this role includes specific major client accounts and carries a sales quota of 500K+ of contract value. Gartner is a sales-driven organization, and the success of our account executives is the fuel that grows the company. #GartnerSales\
\
What you’ll do:\
\
Consult with C-level executives to develop and implement an effective, enterprise-wide strategy that improves the value delivered by Gartner products and services\
\
Manage your accounts toward an outcome of increased customer satisfaction and an increase in retention and account growth\
\
Identify and drive new business opportunities with new-to-Gartner organizations across Asia, targeting large enterprise C-level stakeholders in the human resources function\
\
Handle forecast accuracy on a monthly/quarterly/annual basis\
\
What you need:\
\
Experience with validated consultative sales, with evidence of prior success\
\
Proficiency in account planning and an understanding of territory management\
\
The ability to prospect and run C-level and senior-level relationships within midsize and large organizations\
\
Demonstrated intellect, drive, executive presence and sales acumen\
\
Proven experience building excellent client relationships through offering beneficial, insightful and strategic insights into their businesses\
\
Strong proficiency in computer skills\
\
Excellent written and oral presentation skills\
\
Knowledge of the full life cycle of the sales process, from prospecting to close\
\
Bachelor’s degree preferred"
pdf_location = abspath(join("./", "account-executive-resume-example.pdf"))

data = upload_pdf()
upload_response = upload_file_to_s3(data['upload_url'], pdf_location)
result = post_data(data['download_url'], job_description)
