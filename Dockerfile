FROM public.ecr.aws/lambda/python:3.13

RUN dnf update -y && \
    dnf install -y tesseract tesseract-langpack-jpn && \
    dnf clean all

COPY src/requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install -r requirements.txt

COPY src/ ${LAMBDA_TASK_ROOT}/

CMD ["app.handler"] 