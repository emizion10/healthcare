


var pid;



function add(id){
    if(id=="diagb"){
        var valselected = document.getElementById("icd9dx").value;
        var symselected = document.getElementById("diag").value;
        var arr = symselected.split(",");
        document.getElementById("icd9dx").value="";

        var i = 0;
        var flag = -1;
            while (i < arr.length) {
                if (arr[i] == valselected) {
                    flag = 1;
                    break;
                }
                i = i + 1;
            }
            if (flag == -1) {
                if (symselected.length > 0){
                    document.getElementById("diag").value = arr.join(",") + "," + valselected;
                }
                else{
                    document.getElementById("diag").value = valselected;
                }
            }
            
    }
    if(id=="diseaseb"){
        var valselected = document.getElementById("condition").value;
        var symselected = document.getElementById("disease").value;
        var arr = symselected.split(",");
        document.getElementById("condition").value="";

        var i = 0;
        var flag = -1;
            while (i < arr.length) {
                if (arr[i] == valselected) {
                    flag = 1;
                    break;
                }
                i = i + 1;
            }
            if (flag == -1) {
                if (symselected.length > 0){
                    document.getElementById("disease").value = arr.join(",") + "," + valselected;
                }
                else{
                    document.getElementById("disease").value = valselected;
                }
            }
            
    }
    if(id=="procb"){
        var valselected = document.getElementById("icd9sg").value;
        var symselected = document.getElementById("proc").value;
        var arr = symselected.split(",");
        document.getElementById("icd9sg").value="";

        var i = 0;
        var flag = -1;
            while (i < arr.length) {
                if (arr[i] == valselected) {
                    flag = 1;
                    break;
                }
                i = i + 1;
            }
            if (flag == -1) {
                if (symselected.length > 0){
                    document.getElementById("proc").value = arr.join(",") + "," + valselected;
                }
                else{
                    document.getElementById("proc").value = valselected;
                }
            }
            
    }

    if(id=="medb"){
        var valselected = document.getElementById("rxterms").value;
        var drugstrength = document.getElementById("drug_strengths").value;
        var ptype = document.getElementById("ptype").value;
        var symselected = document.getElementById("med").value;
        var arr = symselected.split(",");
        document.getElementById("rxterms").value="";
        document.getElementById("drug_strengths").value="";


        var i = 0;
        var flag = -1;
            while (i < arr.length) {
                if (arr[i] == valselected) {
                    flag = 1;
                    break;
                }
                i = i + 1;
            }
            if (flag == -1) {
                if (symselected.length > 0){
                    document.getElementById("med").value = arr.join(",") + "," + valselected+" - "+drugstrength+" - ("+ptype+")";
                }
                else{
                    document.getElementById("med").value = valselected+" - "+drugstrength+" - ("+ptype+")";
                }
            }
            
    }
}
