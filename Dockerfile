FROM python:3.11
RUN mkdir /bsf_api
WORKDIR /bsf_api
COPY requirements.txt /bsf_api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /bsf_api/requirements.txt
COPY . .
EXPOSE 8000
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
