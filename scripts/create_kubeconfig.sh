#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MANIFEST="$SCRIPT_DIR/../solution/manifests/serviceaccount.yaml"
KUBECONFIG_OUTPUT="./.kubeconfig"

# Extract the ServiceAccount name and namespace from the manifest
SA_NAME=$(grep 'name:' "$MANIFEST" | awk '{print $2}')
NAMESPACE=$(grep 'namespace:' "$MANIFEST" | awk '{print $2}')
if [[ -z "$NAMESPACE" ]]; then
  NAMESPACE="default"
fi

# Create a token secret for the ServiceAccount (for Kubernetes 1.24+)
SECRET_NAME="${SA_NAME}-token"
echo "Creating token secret $SECRET_NAME for ServiceAccount $SA_NAME in namespace $NAMESPACE..."
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: $SECRET_NAME
  namespace: $NAMESPACE
  annotations:
    kubernetes.io/service-account.name: $SA_NAME
type: kubernetes.io/service-account-token
EOF

# Wait for the token to be populated
echo "Waiting for token to be populated..."
for _ in {1..10}; do
  TOKEN=$(kubectl get secret "$SECRET_NAME" -n "$NAMESPACE" -o jsonpath='{.data.token}' 2>/dev/null || true)
  if [[ -n "$TOKEN" ]]; then break; fi
  sleep 1
done

if [[ -z "$TOKEN" ]]; then
  echo "Error: Token not found in secret after waiting."
  exit 1
fi

# Decode the token and CA cert
TOKEN_DECODED=$(echo "$TOKEN" | base64 -d)
CA_CRT=$(kubectl get secret "$SECRET_NAME" -n "$NAMESPACE" -o jsonpath='{.data.ca\.crt}' | base64 -d | base64)

# Get the current cluster endpoint
CLUSTER_NAME=$(kubectl config view --minify -o jsonpath='{.contexts[0].context.cluster}')
CLUSTER_ENDPOINT=$(kubectl config view --minify -o jsonpath='{.clusters[?(@.name=="'"$CLUSTER_NAME"'")].cluster.server}')

# Create kubeconfig file
echo "Generating kubeconfig at $KUBECONFIG_OUTPUT..."
cat > "$KUBECONFIG_OUTPUT" <<EOF
apiVersion: v1
kind: Config
clusters:
- name: $CLUSTER_NAME
  cluster:
    server: $CLUSTER_ENDPOINT
    certificate-authority-data: $CA_CRT
users:
- name: $SA_NAME
  user:
    token: $TOKEN_DECODED
contexts:
- name: ${SA_NAME}-context
  context:
    cluster: $CLUSTER_NAME
    user: $SA_NAME
    namespace: $NAMESPACE
current-context: ${SA_NAME}-context
EOF

echo "✅ Kubeconfig created at $KUBECONFIG_OUTPUT"