import boto3
from botocore.exceptions import NoCredentialsError, EndpointConnectionError
import os, time
from dotenv import dotenv_values


# Load parameters from .env file
env_vars = dotenv_values('./vars/variables.env')

# Configuração das credenciais da AWS
access_key = env_vars['ACCESS_KEY']
secret_key = env_vars['SECRET_KEY']

# Tempo de espera entre cada upload
wait_for_upload = int(env_vars['WAIT_FOR_UPLOAD'])

# Configuração do cliente S3
s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# Diretório local onde estão os arquivos que serão enviados
upload_folder = env_vars['UPLOAD_FOLDER']

# Nome do bucket S3
bucket_name = env_vars['BUCKET_NAME']

# Get Rasp ID
def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return cpuserial

# Loop para fazer o upload de cada arquivo
def upload_arquivo(upload_folder):
    for arquivo in os.listdir(upload_folder):
        caminho_arquivo = os.path.join(upload_folder, arquivo)
        if os.path.isfile(caminho_arquivo):
            try:
                s3.upload_file(caminho_arquivo, bucket_name, arquivo)
                print(f"Upload do arquivo {arquivo} bem-sucedido!")
            except NoCredentialsError:
                print("Credenciais da AWS não encontradas.")
                return "Error"
            except EndpointConnectionError:
                print("Could not connect to the endpoint URL.")
                return "Error"
            except Exception as e:
                print(f"Erro não esperado: {e}")
                return "Error"
    return None

def delete_local_files(upload_folder, error):
    if error:
        return
    else:
        for arquivo in os.listdir(upload_folder):
            caminho_arquivo = os.path.join(upload_folder, arquivo)
            if os.path.isfile(caminho_arquivo):
                try:
                    os.remove(caminho_arquivo)
                    print(f"Arquivo {arquivo} removido com sucesso!")
                except Exception as e:
                    print(f"Erro não esperado: {e}")
                
def main(wait_for_upload):
    while True:
        print(f"Verificando arquivos em {upload_folder} e enviando para AWS...")
        error = upload_arquivo(upload_folder)
        delete_local_files(upload_folder, error)
        print(f"Próxima verificação em {wait_for_upload} segundos...")
        time.sleep(wait_for_upload)
    
if __name__ == "__main__":
    rasp_id = getserial()
    main(wait_for_upload)