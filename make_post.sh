FP="./_posts/$(date +%Y-%m-%d)-$1.md"

echo "---" >> $FP
echo "layout: post" >> $FP
echo "title: $1" >> $FP
echo "---" >> $FP


vim $FP 
