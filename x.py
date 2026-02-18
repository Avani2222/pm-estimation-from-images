import secrets
secret_key = secrets.token_urlsafe(32)
print(secret_key)
#k2agK7se-zOxhIQ8QO0r6BO9HpC-S6hkPiGa318qxs0
# gcloud run deploy air-quality-api \
#   --image gcr.io/air-sight-app/air-quality-api \
#   --region asia-south1 \
#   --platform managed \
#   --allow-unauthenticated \
#   --memory 1Gi \
#   --timeout 1200 \
#  --set-env-vars DATABASE_URL="postgresql://neondb_owner:npg_0rDFgpYWG2oi@ep-green-breeze-aijn5pai-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",SECRET_KEY="k2agK7se-zOxhIQ8QO0r6BO9HpC-S6hkPiGa318qxs0",
# MAIL_USERNAME=avanigupta2003@gmail.com,
# MAIL_PASSWORD=fltu hxlb iwnl ifxt,
# MAIL_FROM=avanigupta2003@gmail.com
# conf = ConnectionConfig(
#     MAIL_USERNAME="avanigupta2003@gmail.com",
#     MAIL_PASSWORD="fltu hxlb iwnl ifxt",
#     MAIL_FROM="avanigupta2003@gmail.com",
#     MAIL_PORT=587,
#     MAIL_SERVER="smtp.gmail.com",
#     MAIL_STARTTLS=True,
#     MAIL_SSL_TLS=False,
#     USE_CREDENTIALS=True
# )

# gcloud builds submit --tag gcr.io/air-sight-app/air-quality-api
 gcloud run deploy air-quality-api \
  --image gcr.io/air-sight-app/air-quality-api \
  --region asia-south1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi \

  --timeout 1200 \
  --env-vars-file env.yaml

# DATABASE_URL='postgresql://neondb_owner:npg_0rDFgpYWG2oi@ep-green-breeze-aijn5pai-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require' \
# SECRET_KEY='k2agK7se-zOxhIQ8QO0r6BO9HpC-S6hkPiGa318qxs0' \
# MAIL_USERNAME='avanigupta2003@gmail.com' \
# MAIL_PASSWORD='fltu hxlb iwnl ifxt' \
# MAIL_FROM='avanigupta2003@gmail.com' \
# uvicorn src.api:app --reload --host 0.0.0.0 --port 8000