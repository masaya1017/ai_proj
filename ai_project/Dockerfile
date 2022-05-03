FROM python:3.6

ARG project_dir=/project/

ADD requirements.txt $project_dir
ADD image_classifier.h5 $project_dir

WORKDIR $project_dir

ENV FLASK_APP /project/app.py

RUN pip install -r requirements.txt





