import os
import sys
import django
from pathlib import Path

# Adicione o diretório do projeto ao path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xiaomi_proxy.settings')
django.setup()

from django.core.wsgi import get_wsgi_application

wsgi_app = get_wsgi_application()


async def handler(event, context):
    """
    Netlify Functions handler para Django
    """
    # Mapear o evento Netlify para um formato compatível com WSGI
    
    method = event.get('httpMethod', 'GET').upper()
    path = event.get('path', '/')
    headers = event.get('headers', {})
    body = event.get('body', '')
    
    # Criar um environ compatível com WSGI
    environ = {
        'REQUEST_METHOD': method,
        'SCRIPT_NAME': '',
        'PATH_INFO': path,
        'QUERY_STRING': event.get('queryStringParameters', ''),
        'CONTENT_TYPE': headers.get('content-type', ''),
        'CONTENT_LENGTH': headers.get('content-length', '0'),
        'SERVER_NAME': headers.get('host', 'localhost'),
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': None,
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': True,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Adicionar headers ao environ
    for header_name, header_value in headers.items():
        header_name = header_name.upper().replace('-', '_')
        if header_name not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{header_name}'] = header_value
    
    # Executar o WSGI app
    try:
        response_data = []
        status = None
        response_headers = []
        
        def start_response(status_str, headers_list):
            nonlocal status, response_headers
            status = int(status_str.split()[0])
            response_headers = headers_list
            return lambda data: response_data.append(data)
        
        # Chamar o WSGI app
        app_iter = wsgi_app(environ, start_response)
        
        try:
            for data in app_iter:
                response_data.append(data)
        finally:
            if hasattr(app_iter, 'close'):
                app_iter.close()
        
        # Montar a resposta
        response_body = b''.join(response_data)
        
        return {
            'statusCode': status or 200,
            'headers': dict(response_headers),
            'body': response_body.decode('utf-8') if isinstance(response_body, bytes) else response_body,
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': str(e),
        }
