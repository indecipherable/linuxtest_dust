#!/bin/bash
# by flopcoder
#!/bin/bash
PROPERTY_FILE=filename.properties

function getProperty {
  PROP_KEY=$1
  PROP_VALUE=`cat $PROPERTY_FILE | grep "$PROP_KEY" | cut -d'=' -f2`
  echo $PROP_VALUE
}

echo "# Reading property from $PROPERTY_FILE"
DB_USER=$(getProperty "db.username")
DB_PASS=$(getProperty "db.password")
ROOT_LOC=$(getProperty "root.location")
echo $DB_USER
echo $DB_PASS
echo $ROOT_LOC
echo "Writing on DB ... "
mysql -u$DB_USER -p$DB_PASS dbname<<EOFMYSQL

update tablename set tablename.value_ = "$ROOT_LOC" where tablename.name_="Root directory location";
EOFMYSQL
echo "Writing root location($ROOT_LOC) is done ... "
counter=`mysql -u${DB_USER} -p${DB_PASS} dbname -e "select count(*) from tablename where tablename.name_='Root directory location' and tablename.value_ = '$ROOT_LOC';" | grep -v "count"`;

if [ "$counter" = "1" ]
then
echo "ROOT location updated"
fi
