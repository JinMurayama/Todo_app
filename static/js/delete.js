function check() {
    if(window.confirm("本当に削除していいですか?")) {
        window.alert("削除します");
    } else {
        window.alert("キャンセルしました");
        return false;
    }
}