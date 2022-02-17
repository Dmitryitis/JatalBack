//Preloader
let preloader = Vue.createApp({
    data: () => ({
        show: true,
    }),
    mounted() {
        if (Boolean(this.show)) {
            this.showToggle();
        }
    },
    methods: {
        showToggle() {
            setTimeout(() => {
                this.show = false
            }, 700);
        }
    },
});

preloader.mount('#preloader');
//Nav,BurgerMenu
let nav = Vue.createApp({
    data: () => ({
        isActive: false,
        isFixed: false,
        width: 0,
        scrollPosition: 0,
    }),
    methods: {
        toggleMenu() {
            this.isActive = !this.isActive;
            console.log(1);
        },
        updateWidth() {
            this.width = window.innerWidth;
            if (this.width > 768) {
                this.isActive = false;
            }
        },
        onScroll() {
            this.scrollPosition = window.scrollY;
            this.isFixed = this.scrollPosition > 2;
        },
    },
    created() {
        window.addEventListener('resize', this.updateWidth);
        window.addEventListener('scroll', this.onScroll);
    },
    destroyed() {
        window.removeEventListener('resize', this.updateWidth);
    },
});

nav.mount('#app');


//SearchScroll,ShortText
let search = Vue.createApp({
    data: () => ({
        texts: document.querySelectorAll('.posts__text'),
        width: window.innerWidth,
        scrollPosition: 0,
        footerHeight: window.innerHeight,
        info: [],
        inputValue: '',
        searched: [],
    }),
    computed: {
        fixedReady() {
            return this.width > 868 && this.scrollPosition > 550;
        },
    },
    methods: {
        updateWidth() {
            this.width = window.innerWidth;
        },
        updateScroll() {
            this.scrollPosition = window.scrollY;
        },
        searchFunc(e) {
            this.inputValue = e.target.value.trim();
            if (this.inputValue.length !== 0) {
                for (let i in info) {
                    if (this.inputValue.length !== 0 && info[i].title.toLowerCase().includes(this.inputValue.toLowerCase())) {
                        if (!(this.searched.includes(info[i].title))) {
                            this.searched.push(info[i].title);
                        }
                    }
                }
            } else {
                this.searched = [];
            }
        },
        searchInfo() {
            axios.get('/api/posts/')
                .then(function (response) {
                    this.info = response.data;
                });
        },
        clickSearched(i) {
            this.inputValue = this.searched[i];
            this.searched = [];
        }
    },
    created() {
        window.addEventListener('resize', this.updateWidth);
        window.addEventListener('scroll', this.updateScroll);
        this.searchInfo();
    },

});

search.mount('#posts__search-system');

//AutoTypeAnimation
let autoAnimation = Vue.createApp({
    data: () => ({
        speed: 150,
        autoText: '.text-js',
    }),
    mounted() {
        autoType(this.autoText, this.speed);
    },
});
autoAnimation.mount('#log');


//RegistrationForm
let registration = Vue.createApp({
    data: () => ({
        user: {
            username: '',
            email: '',
            password: '',
            rep_password: '',
        },
        patterns: {
            pat_username: /^[а-я]{3,12}|[a-zA-Z0-9_]{3,12}$/,
            pat_email: /^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$/,
            pat_password: /^(?=[#$-/:-?{-~!"^_`\[\]a-zA-Z]*([0-9#$-/:-?{-~!"^_`\[\]]))(?=[#$-/:-?{-~!"^_`\[\]a-zA-Z0-9]*[a-zA-Z])[#$-/:-?{-~!"^_`\[\]a-zA-Z0-9]{4,}$/,
        },
    }),
    computed: {
        formReady() {
            return !!(this.valid_username && this.valid_email && this.valid_password && this.valid_rep_password);
        },
        valid_username() {
            console.log(1);
            return this.patterns.pat_username.test(this.user.username);
        },
        valid_email() {
            return this.patterns.pat_email.test(this.user.email);
        },
        valid_password() {
            return this.patterns.pat_password.test(this.user.password);
        },
        valid_rep_password() {
            return this.user.password === this.user.rep_password;
        }
    },
    methods: {
        clickBtn() {
            if (this.formReady) {
                console.log(this.user);
            }
        },
    },
});
registration.mount('#registr');


function autoType(elementClass, typingSpeed) {
    let thhis = $(elementClass);
    thhis.css({
        "position": "relative",
        "display": "inline-block"
    });
    thhis.prepend('<div class="cursor" style="right: initial; left:0;"></div>');
    thhis = thhis.find(".text-js");
    let text = thhis.text().trim().split('');
    let amntOfChars = text.length;
    let newString = "";
    thhis.text("|");
    setTimeout(function () {
        thhis.css("opacity", 1);
        thhis.prev().removeAttr("style");
        thhis.text("");
        for (let i = 0; i < amntOfChars; i++) {
            (function (i, char) {
                setTimeout(function () {
                    newString += char;
                    thhis.text(newString);
                }, i * typingSpeed);
            })(i + 1, text[i]);
        }
    }, 500);
}

let comments = Vue.createApp({
    methods: {},
})
comments.component('api-comments', {
    data: () => ({
        data_comments: [],
        auth_user: {},
        textComment: '',
        commText: {
            text: '',
            post: -1,
            date_created: '',
            author: '',
        },
        post_id: -1,
        cookie: '',
        textUpdate: {
            text: ''
        },
        activeUpdate: []
    }),
    template: `
    <div class="comments__title">Comments</div>

                <div class="comments__content">
                    <div class="comments__item" v-if="data_comments.length > 0" v-for="(comment,index) in data_comments">
                        <div class="comments__info">
                        <div class="comment__action">
                        <div class="comments__name">
                                    {{comment.author.username}}
                         </div>
                         <span class="comment__actions" v-if="comment.author.id === auth_user.id">
                          <button type="button" class="comment__delete" v-on:click="clickDeleteComment(index)">Удалить</button>
                         <button type="button" class="comment__delete" v-on:click="clickBtnUpdate(index)">Обновить</button>
                            </span>
                       
                            </div>
                           
                            <div class="commemts__date">{{comment.date_created}}</div>
                            <div class="comments__text">
                              {{comment.text}}
                            </div>
                            <div class="comment__update" :class="{'active__update':activeUpdate[index]}"  v-if="comment.author.id === auth_user.id">
                            <textarea name="text" v-model="textUpdate.text" id="text" class="comment__post-tex"></textarea>
                             <div class="comments__post-btn">
                            <button type="button" class="comments__btn--update" v-on:click="update(index)">Обновить</button>
                            <button type="button" class="comments__btn--update" v-on:click="clickBtnCancel(index)">Отмена</button>
                             </div>
                            </div>
                             
                        </div>
                    </div>
              
                    <div class="comments__item" v-if="data_comments.length === 0">
                        <div class="comments__info">
                            No comments
                        </div>
                    </div>
                  
                </div>

                <form method="post" class="comments__post">
              
                    <div class="comments__post-title">Write comments</div>

                    <div class="comments__post-redactor">
                        <div class="comments__post-header">

                        </div>
                        <div class="comments__post-text">
                            <label for="text" class="label__text">Comment</label>
                            <textarea name="text" v-model="textComment" id="text" class="comment__post-tex"></textarea>
                        </div>

                        <div class="comments__post-btn">
                            <button type="button" class="comments__btn" v-on:click="clickBtnComment">Post comment</button>
                        </div>
                    </div>
                </form>
    `,
    methods: {
        async clickBtnComment() {
            this.commText.text = this.textComment;
            this.commText.post = this.post_id
            this.commText.date_created = new Date()
            this.commText.author = this.auth_user.id

            await fetch(`/api/${this.post_id}/comment/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.cookie
                },
                body: JSON.stringify(this.commText)
            }).then(response => response.json())
                .then(result => {
                    console.log(result)
                });

            await fetch(`/api/${this.post_id}/comment/`, {
                method: 'GET',
            }).then(response => response.json())
                .then(result => {
                    this.data_comments = result
                })
            this.textComment = ''
            this.$forceUpdate();
        },
        async clickDeleteComment(index) {
            await fetch(`/api/${this.post_id}/comment/${this.data_comments[index].id}/`, {
                method: 'delete',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.cookie
                },
            }).then(response => response.json())
                .then(result => console.log(result))

            await fetch(`/api/${this.post_id}/comment/`, {
                method: 'GET',
            }).then(response => response.json())
                .then(result => {
                    this.data_comments = result
                })
        },
        clickBtnUpdate(index) {
            this.activeUpdate[index] = true
        },
        clickBtnCancel(index) {
            this.activeUpdate[index] = false
        },
        async update(index) {
            if (this.textUpdate.text !== '') {
                await fetch(`/api/${this.post_id}/comment/${this.data_comments[index].id}/`,
                    {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': this.cookie
                        },
                        body: JSON.stringify(this.textUpdate)
                    }).then(response => response.json())
                    .then(result => console.log(result))

                this.activeUpdate[index] = false

                await fetch(`/api/${this.post_id}/comment/`, {
                    method: 'GET',
                }).then(response => response.json())
                    .then(result => {
                        this.data_comments = result
                    })
            }
        }
    },
    async mounted() {
        let post_id = window.location.href.toString().split('/')
        this.post_id = post_id[post_id.length - 2]
        await fetch('/api/user/', {
            method: 'GET'
        }).then(response => response.json())
            .then(result => this.auth_user = result)
        await fetch(`/api/${post_id[post_id.length - 2]}/comment/`, {
            method: 'GET',
        }).then(response => response.json())
            .then(result => {
                this.data_comments = result
                console.log(this.data_comments)
            });

        await fetch('/api/get-token', {
            method: 'GET'
        }).then(response => response.json())
            .then(result => {
                this.cookie = result.token
            });

        for (let i = 0; i < this.data_comments.length; i++) {
            this.activeUpdate.push(false)
        }
    }
})
comments.mount('#comments')