# 1. Add the Helm repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# 2. Download and unpack the chart source into a local folder
helm pull bitnami/nginx --untar --untardir ./charts


# 3. Render the unpacked chart folder into a single static YAML manifest
helm template my-release ./charts/nginx --include-crds > ./rendered/nginx.yaml