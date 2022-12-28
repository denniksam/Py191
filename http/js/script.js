
document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.querySelector("#login-button");
    if( ! loginButton ) throw "DOMContentLoaded: #login-button not found" ;
    loginButton.addEventListener('click', loginButtonClick ) ;

    const itemsButton = document.querySelector("#items-button");
    if( ! itemsButton ) throw "DOMContentLoaded: #items-button not found" ;
    itemsButton.addEventListener('click', itemsButtonClick ) ;
});
function itemsButtonClick(e) {
    var access_token = window.sessionStorage.getItem( "access_token" ) ;
    if( ! access_token ) {
        alert( "Сначала авторизуйтесь" ) ;
        return ;
    }
    fetch( "/items", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + access_token
        }
    }).then( async r => {
        if( r.status == 401 ) {
            alert( await r.text() ) ;
            // проверка токена отклонена - удалить токен из хранилища
        }
        else if( r.status == 200 ) {
            out.innerText = await r.text() ;
        }
        else {
            console.log( r ) ;
        }
    } ) ;
}
/* Задания:
1. Проверять срок действия токена при его успешном получении
2. При генерировании токена проверять есть ли активный токен для данного пользователя,
    если есть, то не создавать новый, вернуть старый
    * можно создавать новый токен если старый активный, но осталось менее 10 минут
3. При загрузке HTML-страницы (или обновлении) проверять наличие токена в sessionStorage
    если он есть, то не выводить блок авторизации. При негативных ответах сервера,
    проверящего токен, удалять токен из sessionStorage
    * контролировать (выводить таймер обратного отсчета) оставшегося времени авторизации
*/
function loginButtonClick(e) {
    const userLogin = document.querySelector("#user-login");
    if( ! userLogin ) throw "loginButtonClick: #user-login not found" ; 
    const userPassword = document.querySelector("#user-password");
    if( ! userPassword ) throw "loginButtonClick: #user-password not found" ;
    // проверить поля на пустоту, логин - на допустимые символы
    const credentials = btoa( userLogin.value + ':' + userPassword.value ) ;
    fetch( "/auth", {
        method: 'GET',
        headers: {
            'Authorization': 'Basic ' + credentials
        }
    }).then( r => {
        if( r.status != 200 ) {
            alert( "Логин или пароль неправильные" )
        }
        else {
            r.text().then( j => {
                console.log( j ) ;
                // сохраняем полученный токен
                // window.sessionStorage.setItem( "access_token", j.access_token ) ;
            });
        }
    } ) ;

}