FROM jekyll/jekyll:latest as builder
COPY . /_source
WORKDIR /_source
RUN if [[ -d /_source/_site ]]; then rm -r _site; fi && mkdir _site && jekyll build

FROM nginx:alpine
COPY --from=builder /_source/_site /usr/share/nginx/html
