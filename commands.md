# Lambda Setup

- mkdir package
- pip install -r requirements.txt -t ./package
- cp -r application ./package/
- cp -r api ./package/
- cp -r app_secrets ./package/
- cp -r config  ./package/
- cp -r controller  ./package/
- cp -r repository  ./package/
- cp -r service  ./package/
- cp -r main.py ./package/
- cd package
- zip -r ../deployment_package.zip .
- cd ..
