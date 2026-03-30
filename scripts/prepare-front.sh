cd /var/www/tokenguard/frontend
npm run build
rm -rf ../backend/app/static/css ../backend/app/static/js ../backend/app/static/.vite
cp -r dist/* ../backend/app/static/

ls -la ../backend/app/static/
ls -la ../backend/app/static/css/
ls -la ../backend/app/static/js/