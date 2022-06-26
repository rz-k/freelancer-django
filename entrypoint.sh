
#> Export Environment Variable 
# export $(grep -v '^#>' ./config/.env | xargs)

#> Create Database
psql -U postgres -c "CREATE DATABASE freelancer;"  2>/dev/null
