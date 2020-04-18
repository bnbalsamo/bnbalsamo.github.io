FROM jekyll/jekyll:latest as builder
COPY . /srv/jekyll
WORKDIR /srv/jekyll
RUN if [[ -d /srv/jekyll/_site ]]; then rm -r /srv/jekyll/_site; fi && mkdir /srv/jekyll/_site && jekyll build --trace

FROM nginx:alpine
COPY --from=builder /srv/jekyll/_site /usr/share/nginx/html
