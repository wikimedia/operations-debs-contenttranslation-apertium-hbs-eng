INC=$1
PAIR=$2
OUT=testvoc-summary.$PAIR.txt
LOG=testvoc.log

echo -n "" > $OUT;

date >> $OUT
echo -e "===============================================" >> $OUT
echo -e "POS\tTotal\tClean\tWith @\tWith #\tClean %" >> $OUT

# Preliminary, we ignore REGEX everywhere
GLOBAL_EXCLUDE_FILTER=" -e REGEX"
cat $INC | grep -v "$GLOBAL_EXCLUDE_FILTER" > $INC.clean.tmp

# All parts of speech we take into account for testvoc; subtract or add if neccessary
POS_TAGS="abbr adj adv cm cnjadv cnjcoo cnjsub det guio ij n np num pr preadv prn rel vaux vbhaver vblex vbser vbmod"

##
# Does cleanup for one POS tag, according to the grep expression EXCLUDE_FILTER, 
# the output is in $pos_tag.inc.clean.tmp
function cleanup {
    pos_tag=$1;    
    EXCLUDE_FILTER=$2;

    if [ "$EXCLUDE_FILTER" = "" ]; then
	mv $pos_tag.inc.tmp $pos_tag.inc.clean.tmp
    else
	cat $pos_tag.inc.tmp | grep -v $EXCLUDE_FILTER > $pos_tag.inc.clean.tmp
    fi
}

##
# Does summary for $pos_tag, the output is echoed to
# stdout and collected later
function summary {
    local $pos_tag=$1
       
    local TOTAL=`cat $pos_tag.inc.clean.tmp | wc -l`; 
    local AT_INTERSECT_HASH=`cat $pos_tag.inc.clean.tmp | grep '@'  | grep '>  *#' | wc -l`;
    local AT=`cat $pos_tag.inc.clean.tmp | grep '@'  | wc -l`;
    local HASH=`cat $pos_tag.inc.clean.tmp | grep '>  *#' | wc -l`;

    local UNCLEAN=`calc $AT+$HASH-$AT_INTERSECT_HASH`;
    local CLEAN=`calc $TOTAL-$UNCLEAN`;
    local PERCLEAN=`calc $UNCLEAN/$TOTAL*100 |sed 's/^\W*//g' | sed 's/~//g' | head -c 5`;
    local TOTPERCLEAN="0";
    echo $PERCLEAN | grep "Err" > /dev/null;
    if [ $? -eq 0 ]; then
	TOTPERCLEAN="100";
    else
	TOTPERCLEAN=`calc 100-$PERCLEAN | sed 's/^\W*//g' | sed 's/~//g' | head -c 5`;
    fi

    echo -e $TOTAL";"$pos_tag";"$CLEAN";"$AT";"$HASH";"$TOTPERCLEAN;    
}

for pos_tag in $POS_TAGS; do
    cat $INC.clean.tmp | grep "<$pos_tag>" > $pos_tag.inc.tmp
    EXCLUDE_FILTER="";
    if [ "$pos_tag" = "det" ]; then
	EXCLUDE_FILTER="-e '<n>' -e '<np>'"
    elif [ "$pos_tag" = "preadv" ]; then
	EXCLUDE_FILTER="-e '<adj>' -e '<adv>'"
    elif [ "$pos_tag" = "adv" ]; then
	EXCLUDE_FILTER="-e '<adj>' -e '<v'"
    elif [ "$pos_tag" = "cnjsub" ]; then
	EXCLUDE_FILTER="-e '<v'"
    elif [ "$pos_tag" = "prn" ]; then
	EXCLUDE_FILTER="-e '<v'"
    elif [ "$pos_tag" = "vbser" ]; then
	EXCLUDE_FILTER="-e '<pp' -e '<vbm'"
    elif [ "$pos_tag" = "vbhaver" ]; then
	EXCLUDE_FILTER="-e '<pp' -e '<vbm'"
    elif [ "$pos_tag" = "pr" ]; then
	EXCLUDE_FILTER="-e '<prn' -e '<ger'"
    elif [ "$pos_tag" = "rel" ]; then
	EXCLUDE_FILTER="-e '<pr'"
    elif [ "$pos_tag" = "adj" ]; then
	EXCLUDE_FILTER="-e '<np'"
    elif [ "$pos_tag" = "vbmod" ]; then
	EXCLUDE_FILTER="-e '<vbl'"
    fi

    cleanup "$pos_tag" "$EXCLUDE_FILTER"
    summary "$pos_tag"

done | sort -gr | awk -F';' '{print $2"\t"$1"\t"$3"\t"$4"\t"$5"\t"$6}' >> $OUT

# Cleanup
rm *.tmp

echo -e "===============================================" >> $OUT
cat $OUT;
