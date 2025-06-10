## using the pyhton 3.12 image
FROM python:3.12-slim

RUN useradd -ms /bin/bash user

WORKDIR /home/user/app

ENV PATH="/home/user/.local/bin:${PATH}"
 
COPY --chown=user:user . .

USER user

RUN pip install --user -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]