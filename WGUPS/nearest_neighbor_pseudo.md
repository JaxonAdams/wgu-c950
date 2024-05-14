
function PlotDeliveryRoute(truck)
    Initialize an empty list "route"
    Initialize a set "unvisited_addresses" with each package address on the truck

    current_location = HUB
    while length(unvisited_addresses) != 0
        next_address = null
        min_distance = infinity

        for each address in unvisited_addresses:
            distance = distance between current_location and address
            if distance < min_distance
                min_distance = distance
                next_address = address
            end if
        end for

        append next_address to route
        remove next_address from unvisited_addresses
        current_location = next_address
    end while

    append HUB to route
end function