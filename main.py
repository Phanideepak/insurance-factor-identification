from application import create_app
from mangum import Mangum

app = create_app()

# if __name__ == 'main':
#     uvicorn.run('main:app', host='127.0.0.1', port = 11339, reload= True)

handler = Mangum(app)