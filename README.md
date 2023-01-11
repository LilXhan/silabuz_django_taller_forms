
# Taller formularios

## Templates
----
Para poder crear nuestros primeros formularios, necesitamos lo siguiente:

-   Crear la carpeta `templates` dentro de `myapp`.

Para este ejemplo dentro de `myapp/templates/form.html` añadimos lo siguiente.

> 👀 Crear `form.html`

```html
<form action = "" method = "post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit">
</form>
```

## Creando el form
---
Luego creamos un archivo `forms.py` dentro de `myapp`, y dentro de este añadimos.

```python
from django import forms

# creating a form
class InputForm(forms.Form):

    aula = forms.CharField(max_length = 3)
    hora_entrada = forms.TimeField(
        help_text="Ingrese la hora en formato HH:MM"
        )
```

-   `help_text` renderiza una especie de label que sirva como guía acerca del input.
-  `max_length` indica el tamaño máximo del campo.

### Tipos de campos

Para nuestro form encontramos los siguientes campos:

-   Charfield: El tipo de datos de ingreso es string.
    -   max_length: Indica el tamaño máximo del campo.
    
-   TimeField: Permite el ingreso de datos en el siguiente formato.
    -   `HH:MM`
    -   `HH:MM:SS`


## Creando la vista
---
Ahora que tenemos creada el modelo de nuestro form, añadimos lo siguiente en `myapp/views.py`.

```python
# ...
from .forms import InputForm

# ...

def form_view(request):
    context = {}
    context['form']= InputForm()
    return render(request, "form.html", context)
```

-   La función `render` trabaja de la misma forma que `render_template`(Flask), por eso es necesario tener nuestra carpeta de templates.
-   `context` sirve para añadir las distintas variables que enviaremos a nuestro template, en este caso todo nuestro `InputForm`
-   `request` sirve para diferenciar el tipo de operación CRUD que hagamos, GET, POST, UPDATE, DELETE.

Creada nuestra nueva vista, necesitamos añadir la nueva ruta que acceda a nuestro form.

### Añadiendo la nueva ruta

Dentro de `myapp/urls.py`

```python
# ...
from .views import form_view

urlpatterns = [
    path("", home_page_view, name="home"),

    # Nueva url a form
    path("form", form_view, name="form")
    ]
```


💡 el parámetro `name`, permite que se pueda referenciar a la ruta por su nombre y no por el url. Más información en [name Parameter](https://stackoverflow.com/questions/12818377/django-name-parameter-in-urlpatterns)

## Resultado final
---
Luego de completar todos los pasos, ejecutamos nuestro servidor y accedemos a la ruta `/form`, en la cual obtenemos el siguiente resultado.

![[20230111131447.png]]

## Recepción de información
---
Ahora que tenemos el input creado, podemos recibir la información ingresada. Podemos recibirlas mediante solicitudes POST, que se realicen.

Primero modificamos nuestra vista que renderiza el form y realizamos la siguiente modificación.

```python
def form_view(request):
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            return HttpResponse(
                "Ingresaste el aula "
                + form.cleaned_data["aula"]
                + " y tiene la hora de entrada "
                + str(form.cleaned_data["hora_entrada"])
            )
    # ...
```

Al momento obtener la solicitud de tipo POST, creamos un objeto del mismo tipo que el form utilizado. Esto se hace ya que el framework de formularios muy aparte de servir para la validación de campos, transforma la información recibida a tipos de datos Python en base a la vista que creamos.

Luego con el objeto creado, validamos la información y de ahí retornamos los datos recibidos.

-   `cleaned_data`: Retorna un diccionario con los datos que han sido validados, donde la llave es el nombre del campo y el valor el dato ingresado en el input.

> 💡 `cleaned_data` al retornar un diccionario con los valores del input, los tipos de datos se mantienen al ser retornados. En este caso `form.cleaned_data["hora_entrada"]` retornaría un tipo de dato `TimeField()`.

Al ejecutar deberíamos obtener lo siguiente.


![[20230111131602.png]]

![[20230111131625.png]]

## Rutas dinámicas
---
Al igual que en flask, podemos recibir parámetros por el url. Crearemos una nueva ruta en `myapp/urls.py`. Importando la nueva vista.

```python
# ...
from .views import aula_view

urlpatterns = [
    # ...
    # Nueva url dinámica
    path("form/<aula>", aula_view, name="aula")
    ]
```

En este caso el parámetro dinámico está definido por `< >`, este nombre debe ser enviado como parámetro dentro de la vista que lo vaya a utilizar.

Luego añadimos `aula_view` en `myapp/views.py`.

```python
def aula_view(request, aula):
    return HttpResponse(f"El parámetro enviado por URL es {aula}")
```

Tanto el parámetro de la función como el nombre dentro de la URL coinciden.

Ahora, en nuestra en `form_view` realizamos la siguiente modificación para hacer uso de nuestra nueva vista y añadimos el siguiente import.

```python
# ...
from django.shortcuts import redirect

def form_view(request):
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            return redirect("aula", aula= form.cleaned_data["aula"])
    # ...
```

Al volver a ejectuar obtenemos lo siguiente.

![[20230111131751.png]]

![[20230111131810.png]]

Ya recibimos información por parámetro de URL, pero ¿cómo enviamos información adicional sin hacer uso del url?

## Entorno de sesiones
---
Te permite almacenar y recuperar cualquier información en base a la sesión del usuario. Por lo que, podemos utilizarlo para enviar la hora de entrada a nuestra url dinámica.

Modificamos `form_view`.

```python
def form_view(request):
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            # Uso de la sesión para añadir un nuevo dato
            request.session['hora_entrada'] = str(form.cleaned_data["hora_entrada"])

            return redirect("aula", aula= form.cleaned_data["aula"])
    # ...
```

Con el dato serializado dentro de la sesión, podemos hacer uso de el dentro de nuestra ruta dinámica.

>  ⚠️ Todos los datos serializados deben ser aceptados por el formato JSON.

Modificando `aula_view`.

```python
def aula_view(request, aula):
    # Uso de la sesión para obtener el dato
    hora_entrada = request.session["hora_entrada"]

    return HttpResponse(
        f"El parámetro enviado por URL es {aula} y recibimos del request el horario en {hora_entrada}"
    )
```

Si volvemos a ejecutar la solicitud, obtenemos.

![[20230111131934.png]]

![[20230111131938.png]]

## Tarea
---
Para este taller, crear un formulario en base al modelo Alumno, la ruta para este formulario debe ser `/formAlum`.

Dentro de los campos se debe tener:

-   Nombre del alumno
    
-   Apellido del alumno
    
-   Id del aula a la que pertenece
    

Luego, cree una ruta dinámica que reciba el nombre del alumno como parámetro. Ejemplo `/formAlum/Juan`. Además en la ruta dinámica obtenga todos los datos ingresados en el formulario por `request.session`.

Los datos a recibir dentro de la vista con ruta dinámica son los siguientes:

-   Apellido del Alumno
    
-   Id del aula a la que pertenece
    

### Opcional

Aplicar la misma lógica del item anterior, pero para el modelo profesor.

-   Ruta formulario: `/formProf`
    
-   Ruta dinámica; `/formProf/<first_name>`


---
Los mismos links del repositorio [github](https://github.com/LilXhan/silabuz_django_taller_modelos)
