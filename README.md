# Automatizacion-de-certificados
En este proyecto se busca solucionar un problema de una dependencia de gobierno, la cual todavia realiza de manera manual tareas repetitivas las
cuales se pueden optimizar de manera en que solo sean vigiladas por el encargado que anteriormente realizaba dicha tarea, la cuestión en si es que dicha dependencia generaba y entregaba certificados de eventos de gobierno publico o privado, mediante una base de datos que se generaba en dicho evento para saber el nombre completo y direccion de email a donde mandar dicho certificados, el problema es que al ser una tarea manual con algunas veces demasiados registros que completar se volvia bastante extenso por lo que optaron en una mejora tecnologica que facilitara dicha tarea, aqui es donde desarrollo una aplicacion que se pueda ejecutar directamente en un equipo por lo que no depende de algun servidor donde este alojada y a su vez esto hace que dicha aplicacion este totalmente ajustada a las posibilidades de dicho equipo, la aplicación consiste en que en base a la antes mencionada base de datos(un excel) y una plantilla que la dependencia ya tenga destinada para el evento, la aplicacion reescriba uno por uno los nombres que se encuentren en el registro y se manden correspondientemente al correo al cual se liga el nombre, de esta manera un procesos que antes tomaba dias o semanas completas sea resuelto en cuestión de minutos, asi permitiendo que el personal
pueda dirigir sus esfuerzos en otros ambitos de mayor precisión humana.

# Herramientas usadas
Python
yagmail
pandas
customtkinter
