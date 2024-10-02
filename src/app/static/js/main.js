
function toggleFields() {
    var selectedOption = document.getElementById("cloud_platform").value;

    // Mostrar u ocultar los campos según la opción seleccionada
    if (selectedOption === "azure") {
        document.getElementById("azure_provider").style.display = "block";

        var selectedCloudProvider = document.getElementById("azure_platform").value;
        if (selectedCloudProvider === "azure_sql_database") {
            document.getElementById("databaseField").style.display = "block";
            document.getElementById("serverField").style.display = "block";
            document.getElementById("userField").style.display = "block";
            document.getElementById("passwordField").style.display = "block";

            document.getElementById("database_server").placeholder = "server-name.database.windows.net";
            document.getElementById("database_name").placeholder = "database name";

        } else if (selectedCloudProvider === "azure_cosmos") {
            document.getElementById("databaseField").style.display = "block";
            document.getElementById("serverField").style.display = "block";
            document.getElementById("userField").style.display = "block";
            document.getElementById("passwordField").style.display = "block";

            document.getElementById("database_server").placeholder = "server-name.database.windows.net";
            document.getElementById("database_name").placeholder = "database name";
        } else if (selectedCloudProvider == "azure_db_mysql") {
            document.getElementById("databaseField").style.display = "block";
            document.getElementById("serverField").style.display = "block";
            document.getElementById("userField").style.display = "block";
            document.getElementById("passwordField").style.display = "block";

            document.getElementById("database_server").placeholder = "server-name.database.windows.net";
            document.getElementById("database_name").placeholder = "database name";
        }

    } else if (selectedOption === "aws") {
        // Aquí puedes agregar lógica para AWS si es necesario
    } else if (selectedOption === "oracle") {
        // Aquí puedes agregar lógica para Oracle si es necesario
    } else if (selectedOption === "local") {
        // Aquí puedes agregar lógica para Local si es necesario
    } else {
        // Ocultar todos los campos si no se selecciona ninguna opción válida
        document.getElementById("urlField").style.display = "none";
        document.getElementById("hostField").style.display = "none";
        document.getElementById("schemaField").style.display = "none";
        document.getElementById("userField").style.display = "none";
        document.getElementById("passwordField").style.display = "none";
    }
}

function showTable(){
    document.write("Hola");
    document.getElementById("data_table").style.display = "block";


}

