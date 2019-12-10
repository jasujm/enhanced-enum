// Minimalistic implementation of enum iterator and range for pre-ranges TS C++

#ifndef ENHANCED_ENUM_DETAILS_RANGES_HH_INCLUDED_
#define ENHANCED_ENUM_DETAILS_RANGES_HH_INCLUDED_

#include <iterator>

namespace enhanced_enum {
namespace details {

template<typename EnhancedEnum>
struct enum_iterator {
    using difference_type = std::ptrdiff_t;
    using value_type = EnhancedEnum;
    using reference = const EnhancedEnum&;
    using pointer = const EnhancedEnum*;
    using iterator_category = std::random_access_iterator_tag;

    enum_iterator() = default;
    explicit constexpr enum_iterator(EnhancedEnum value) noexcept : value {value} {};

    constexpr reference operator*() const noexcept { return value; }
    constexpr pointer operator->() const noexcept { return &value; }

    constexpr enum_iterator& operator+=(difference_type n) noexcept
    {
        value = static_cast<typename EnhancedEnum::label_type>(integer() + n);
        return *this;
    }

    constexpr enum_iterator& operator-=(difference_type n) noexcept
    {
        return *this += (-n);
    }

    constexpr enum_iterator& operator++() noexcept
    {
        return *this += 1;
    }

    constexpr enum_iterator operator++(int) noexcept
    {
        const auto tmp = enum_iterator {value};
        ++*this;
        return tmp;
    }

    constexpr enum_iterator& operator--() noexcept
    {
        return *this -= 1;
    }

    constexpr enum_iterator operator--(int) noexcept
    {
        const auto tmp = enum_iterator {value};
        --*this;
        return tmp;
    }

    constexpr difference_type operator-(enum_iterator other) const noexcept
    {
        return integer() - other.integer();
    }

    constexpr reference operator[](difference_type n) const noexcept
    {
        return *(*this + n);
    }

private:

    constexpr difference_type integer() const noexcept
    {
        return static_cast<difference_type>(value.get());
    }

    EnhancedEnum value;
};

template<typename EnhancedEnum>
constexpr bool operator==(
    enum_iterator<EnhancedEnum> lhs, enum_iterator<EnhancedEnum> rhs) noexcept
{
    return *lhs == *rhs;
}

template<typename EnhancedEnum>
constexpr bool operator!=(
    enum_iterator<EnhancedEnum> lhs, enum_iterator<EnhancedEnum> rhs) noexcept
{
    return !(lhs == rhs);
}

template<typename EnhancedEnum>
constexpr bool operator<(
    enum_iterator<EnhancedEnum> lhs, enum_iterator<EnhancedEnum> rhs) noexcept
{
    return *lhs < *rhs;
}

template<typename EnhancedEnum>
constexpr bool operator<=(
    enum_iterator<EnhancedEnum> lhs, enum_iterator<EnhancedEnum> rhs) noexcept
{
    return !(rhs < lhs);
}

template<typename EnhancedEnum>
constexpr bool operator>(
    enum_iterator<EnhancedEnum> lhs, enum_iterator<EnhancedEnum> rhs) noexcept
{
    return rhs < lhs;
}

template<typename EnhancedEnum>
constexpr bool operator>=(
    enum_iterator<EnhancedEnum> lhs, enum_iterator<EnhancedEnum> rhs) noexcept
{
    return !(lhs < rhs);
}

template<typename EnhancedEnum>
constexpr enum_iterator<EnhancedEnum> operator+(
    enum_iterator<EnhancedEnum> it,
    typename enum_iterator<EnhancedEnum>::difference_type n) noexcept
{
    return it += n;
}

template<typename EnhancedEnum>
constexpr enum_iterator<EnhancedEnum> operator+(
    typename enum_iterator<EnhancedEnum>::difference_type n,
    enum_iterator<EnhancedEnum> it) noexcept
{
    return it += n;
}

template<typename EnhancedEnum>
constexpr enum_iterator<EnhancedEnum> operator-(
    enum_iterator<EnhancedEnum> it,
    typename enum_iterator<EnhancedEnum>::difference_type n) noexcept
{
    return it -= n;
}

template<typename EnhancedEnum>
struct enum_range
{
    using value_type = EnhancedEnum;
    using reference = const EnhancedEnum&;
    using const_reference = const EnhancedEnum&;
    using iterator = enum_iterator<EnhancedEnum>;
    using const_iterator = enum_iterator<EnhancedEnum>;
    using difference_type = std::ptrdiff_t;
    using size_type = std::size_t;

    constexpr enum_range(iterator first, iterator last) noexcept :
        first {first},
        last {last}
    {};

    constexpr iterator begin() const noexcept { return first; }
    constexpr iterator end() const noexcept { return last; }

    constexpr size_type size() const noexcept
    {
        return static_cast<size_type>(last - first);
    }

private:
    iterator first;
    iterator last;
};

}
}

#endif // ENHANCED_ENUM_DETAILS_RANGES_HH_INCLUDED_
