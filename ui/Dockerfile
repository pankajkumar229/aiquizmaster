FROM node:lts-alpine as node

RUN mkdir /ui
COPY . /ui
# COPY ./staticserver /staticserver

WORKDIR /ui
# RUN rm -rf staticserver/ && apk add python && apk add rsync && apk add py-pip && pip install shyaml && 
RUN chmod 755 ./start.sh && export NODE_OPTIONS=--max_old_space_size=8096 && yarn install 
# RUN npm config set unsafe-perm true
EXPOSE 3000
# ENTRYPOINT yarn start
ENTRYPOINT ./start.sh
# ENTRYPOINT ./start-dev.sh

# ---------Troubleshooting tips
# run
# docker container ls --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}" -a | grep 3000
# to check if anything running on port 3000 and docker stop if running
# docker run -d -v ~/product/courses/components:/courses/components -v ~/product/courses/pages:/courses/pages -v ~/product/courses/public:/courses/public -v ~/product/courses/styles:/courses/styles -v ~/product/courses/util:/courses/util mayank/courses

# docker inspect 54024b24525a | grep 172 
# tmux
# sudo socat TCP6-LISTEN:3000,su=nobody,fork,reuseaddr TCP4:172.17.0.2:3000

# exit tmux -- 