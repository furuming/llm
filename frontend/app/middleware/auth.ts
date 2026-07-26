import type { User } from "~/types/User"

export default defineNuxtRouteMiddleware(async (to, from) => {

    const auth = useAuth()
    const user = auth.get()

    console.log("auth middleware", user.value)

    // userが未設定の場合は取得をトライ
    if( !user.value ){

        try{
            const u = await $fetch<User>("/api/auth/get-user")
            console.log("auth middleware u", u)
            auth.set(u)

        } catch(e){

            return navigateTo('/login') 
        }
        
    }

})