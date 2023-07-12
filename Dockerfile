FROM python:3.10.11-slim as base
# Path: /app
WORKDIR /app
COPY . /app/
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    apt-get install -y lsb-release curl gpg && \
    apt-get install -y ffmpeg libsm6 libxext6  
RUN curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list
RUN apt-get install -y redis
RUN pip install -r requirements.txt

EXPOSE 8000
EXPOSE 6379
ARG BCRYPT_KEY
ARG DJANGO_SECRET_KEY
ARG DEBUG
ARG CLOUDINARY_CLOUD_NAME
ARG CLOUDINARY_API_KEY
ARG CLOUDINARY_API_SECRET
ARG JWT_SECRET_KEY
ARG SENDER_EMAIL_ID
ARG SENDER_EMAIL_APP_PASSWORD

ENV BCRYPT_KEY=$BCRYPT_KEY
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
ENV DEBUG=$DEBUG
ENV CLOUDINARY_CLOUD_NAME=$CLOUDINARY_CLOUD_NAME
ENV CLOUDINARY_API_KEY=$CLOUDINARY_API_KEY
ENV CLOUDINARY_API_SECRET=$CLOUDINARY_API_SECRET
ENV JWT_SECRET_KEY=$JWT_SECRET_KEY
ENV SENDER_EMAIL_ID=$SENDER_EMAIL_ID
ENV SENDER_EMAIL_APP_PASSWORD=$SENDER_EMAIL_APP_PASSWORD
RUN cd SRAM/SRAM/ && touch .env && echo "BCRYPT_KEY=$BCRYPT_KEY" >> .env && echo "DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY" >> .env && echo "DEBUG=$DEBUG" >> .env && echo "CLOUDINARY_CLOUD_NAME=$CLOUDINARY_CLOUD_NAME" >> .env && echo "CLOUDINARY_API_KEY=$CLOUDINARY_API_KEY" >> .env && echo "CLOUDINARY_API_SECRET=$CLOUDINARY_API_SECRET" >> .env && echo "JWT_SECRET_KEY=$JWT_SECRET_KEY" >> .env && echo "SENDER_EMAIL_ID=$SENDER_EMAIL_ID" >> .env && echo "SENDER_EMAIL_APP_PASSWORD=$SENDER_EMAIL_APP_PASSWORD" >> .env
CMD redis-server & ./entrypoint.sh