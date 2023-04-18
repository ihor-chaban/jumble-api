FROM python:3.9.16-alpine

RUN pip install --upgrade pip

RUN adduser -D myuser

USER myuser

WORKDIR /home/myuser

COPY --chown=myuser:myuser ["./app", "./app"]
COPY --chown=myuser:myuser ["./requirements.txt", "./"]

RUN pip install --user -r requirements.txt

ENV PATH="/home/myuser/.local/bin:${PATH}"

EXPOSE 8000

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
