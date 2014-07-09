! explicit_euler.f95
! subroutine to compute explicit Euler solution of kinetic equations
! July 2014

subroutine solve( N_t, N_c, N_s, w_0, w_f, T_s, logA, E, nu, beta, w_s )
    
    implicit none

    ! inputs/outputs
    integer, intent(in)                 :: N_t      ! number of time steps
    integer, intent(in)                 :: N_c      ! number of components
    integer, intent(in)                 :: N_s      ! number of solution values
    real, intent(in), dimension(N_c)    :: w_0
    real, intent(in)                    :: w_f
    real, intent(in), dimension(N_s)    :: T_s
    real, intent(in), dimension(N_c-1)  :: logA
    real, intent(in), dimension(N_c-1)  :: E
    real, intent(in), dimension(N_c-1)  :: nu
    real, intent(in)                    :: beta
    real, intent(out), dimension(N_s)   :: w_s

    ! local variables
    integer                 :: i, j, k
    real, dimension(N_c-1)  :: r
    real, dimension(N_c)    :: w
    real                    :: dT
    real                    :: T

    w = w_0
    dT = (T_s(N_s) - T_s(1))/N_t
    T = T_s(1)
    w_s(1) = 1.
    k = 2

    do j = 2, N_t

        ! compute weight fractions at time step j

        r(1)    = 10.**logA(1)*w(1)*exp(-E(1)/(8.314*T))/beta
        r(1)    = min(r(1), w(1)/dT)
        w(1)    = w(1) - dT*r(1)

        do i = 2, N_c - 1

            r(i) = 10.**logA(i)*w(i)*exp(-E(i)/(8.314*T))/beta
            r(i) = min(r(i), w(i)/dT + nu(i-1)*r(i-1))
            w(i) = w(i) - dT*(r(i) - nu(i-1)*r(i-1))

        end do

        w(N_c) = min(w_f, w(N_c) - dT*(-nu(N_c-1)*r(N_c-1)))
        
        ! update temperature 
        T = T + dT

        ! store solution weights if necessary
        if ( (T >= T_s(k)).and.((T-dT) < T_s(k)) ) then
            
            w_s(k) = sum(w)
            k = k + 1

        end if
    
    end do

end subroutine solve
