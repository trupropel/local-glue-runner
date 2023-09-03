FROM amazon/aws-glue-libs:glue_libs_4.0.0_image_01

USER root
RUN groupadd --g 1024 groupcontainer
RUN usermod -a -G groupcontainer glue_user

USER glue_user
WORKDIR /home/glue_user/workspace
COPY ./Pipfile* .

ENV PACKAGE="/home/glue_user/workspace/helpers"
ENV PYTHONPATH="${PYTHONPATH}:$PACKAGE"
ENV PATH="/home/glue_user/spark/bin:/home/glue_user/.local/bin:$PATH"

RUN pip3 install pipenv

RUN python3 -m pipenv install
