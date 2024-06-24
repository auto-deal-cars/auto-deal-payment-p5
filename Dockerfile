FROM public.ecr.aws/lambda/python:3.10

COPY ./requirements.txt ./
COPY ./payment ${LAMBDA_TASK_ROOT}/payment

RUN pip install --no-cache-dir -r requirements.txt

CMD ["payment.adapters.controllers.pay_controller.create_payment"]
