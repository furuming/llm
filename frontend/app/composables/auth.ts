import type { User } from "~/types/User"



const auth = useState<User|undefined>('auth', ()=>undefined)

export const useAuth = () => {

    const get = () => auth

    const set = (user: User) => {
        auth.value = user
    }

    return { get, set}

}

