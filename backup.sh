# 백업 경로 설정
LOCAL_BACKUP_DIR="/home/fdpiee/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$LOCAL_BACKUP_DIR/db_backup_$TIMESTAMP.sql"

# MySQL 백업 수행
mysqldump -u root -p'your_password' stock_db > "$BACKUP_FILE"
echo "로컬 백업 완료: $BACKUP_FILE"

# 7일 이상 된 파일 삭제
find "$LOCAL_BACKUP_DIR" -type f -name "*.sql" -mtime +7 -exec rm {} \;

