BEGIN {
print "IP Address\tAccess Count\tNumber of sites";
}
{
Ip[$1$2]++;
}
END{
for (var in Ip)
    print var,"\t",Ip[var];
}