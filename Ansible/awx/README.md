## Install AWX on Kubernetes cluster running on Windows 11 DOcker Desktop

Followed below blog:
https://chrisjhart.com/TLDR-AWX-Minikube-Ubuntu-2204/

```bash
mkdir awx
# Create kustomization file
cat <<EOF > awx/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  # Find the latest tag here: https://github.com/ansible/awx-operator/releases
  - github.com/ansible/awx-operator/config/default?ref=2.5.3

# Set the image tags to match the git version from above
images:
  - name: quay.io/ansible/awx-operator
    newTag: 2.5.3

# Specify a custom namespace in which to install AWX
namespace: awx
EOF

# Apply kustomization file
kubectl apply -k awx/

# Modify kubectl namespace
kubectl config set-context --current --namespace=awx

# Wait until awx-operator pod is running and fully ready. Control+C to break out of this command.
kubectl get pods -w

# Create AWX resource file
cat <<EOF > awx/awx.yaml
---
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx
spec:
  service_type: nodeport
EOF

# Modify kustomization file to include AWX resource file
cat <<EOF > awx/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  # Find the latest tag here: https://github.com/ansible/awx-operator/releases
  - github.com/ansible/awx-operator/config/default?ref=2.5.3
  - awx.yaml

# Set the image tags to match the git version from above
images:
  - name: quay.io/ansible/awx-operator
    newTag: 2.5.3

# Specify a custom namespace in which to install AWX
namespace: awx
EOF

# Re-apply kustomization file to pick up AWX resource file changes
kubectl apply -k awx/

# Watch installation process through logs. This may take a few minutes to complete. Wait until 
# you see the following:
#
# {"level":"info","ts":"2023-09-24T17:05:16Z","logger":"KubeAPIWarningLogger","msg":"unknown field \"status.conditions[1].ansibleResult\""}
# 
# Use Control+C to break out of this command once installation is complete.
kubectl logs -f deployments/awx-operator-controller-manager -c awx-manager

# Access in browser or curl
curl http://192.168.49.2:31227

# If you're running Minikube locally, you can access the AWX web interface by running the
# following command:
# minikube service awx-service -n awx

# Confirm the IP output by the above command is reachable via curl (or simply access in your
# browser)
# curl http://192.168.49.2:31227

# If you're running Minikube on a remote server, you'll need to port forward pod's web service
# port number to external IP of Minikube host. The below command exposes port 8080 on your Minikube
# cluster's external IP address. You can then access the AWX web interface by navigating to
# http://<minikube-external-ip>:8080 in your browser.
# kubectl port-forward svc/awx-service --address 0.0.0.0 8080:80 &> /dev/null &

# Get the password for the AWX admin user (default username is "admin") to log into the AWX web
# interface.
# kubectl get secret awx-admin-password -o jsonpath="{.data.password}" | base64 --decode; echo

```