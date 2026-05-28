#-------------------ConfigMap-----------------------------#
# Step 1: Create configmap.yaml file and apply it

# Step 3: Create deployment-configmap.yaml file and apply it
- Note that there are two ways to injest configs

#--------------------Secrets--------------------------------#

# Step 1: First generate base64-encoded strings on your terminal:bash
```bash
echo -n "super-secret-password" | base64
# Output: c3VwZXItc2VjcmV0LXBhc3N3b3Jk
```
```bash
echo -n "xyz-api-token-123" | base64
# Output: eHl6LWFwaS10b2tlbi0xMjM=
```
# Step 2: Create secret.yaml file and apply it

# Step 3: Create deployment-secret.yaml file and apply it
- Note that there are two ways to injest secrets
