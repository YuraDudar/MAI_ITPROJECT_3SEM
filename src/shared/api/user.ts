import { BASE_API_URL } from "../consts/api"
import { User } from "../types/entity"

export const login = (user: Omit<User, 'username' | 'id'>): Promise<{access_token: string}> => {
  return fetch(`${BASE_API_URL}/login`, {
    headers: {
      'content-type': 'application/json',
    },
    method: 'PUT',
    body: JSON.stringify(user),
  }).then(res => res.json());
}

export const register = (user: Omit<User, 'id'>): Promise<User> => {
  console.log(user)
  return fetch(`${BASE_API_URL}/register`, {
    headers: {
      'content-type': 'application/json',
    },
    method: 'POST',
    body: JSON.stringify(user),
  }).then(res => res.json());
}