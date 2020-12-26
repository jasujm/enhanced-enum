/** \file
 *
 * \brief The main header for the Enhanced Enum library
 */

#ifndef ENHANCED_ENUM_HH_INCLUDED_
#define ENHANCED_ENUM_HH_INCLUDED_

#include "details/ranges.hh"

#include <array>
#include <optional>
#include <type_traits>

/** \brief The main namespace for the Enhanced Enum library
 */
namespace enhanced_enum {

/** \brief Base class for the enhanced enumeration types
 *
 * The essential functionality of an enhanced enum type is implemented
 * in this class. A type gains the capabilities of an enhanced enum by
 * deriving from this class, and defining a static constant array
 * called \c values, as described in the user guide. The code for the
 * derived class is intended to be autogenerated to ensure conformance
 * with the requirements.
 *
 * There is an order-preserving isomorphism between the instances of
 * \c EnhancedEnum, and the enumerators of the underlying \c
 * LabelEnum. Thus, conceptually the instances of \c EnhancedEnum are
 * its enumerators, and will be called so in the documentation.
 *
 * An enumerator of \c EnhancedEnum simply stores the value of its
 * label enumerator as its only member. Consequently, most of the
 * traits of \c LabelEnum are also traits of the \c EnhancedEnum type:
 * enhanced enumerations are regular, totally ordered, trivial, and
 * layout compatible with their underlying label enumerators.
 *
 * It is assumed that the definition of the derived class is
 * compatible with the requirements imposed by the library. Most
 * notably the derived class must not have any non-static data members
 * or other non-empty base classes. The intended way to ensure
 * compatibility is to autogenerate the definition.
 *
 * \warning Trying to use an instance of a class derived from \ref
 * enum_base not meeting the requirements imposed by the library
 * results in undefined behavior.
 *
 * \tparam EnhancedEnum The enhanced enumeration. The base class template
 * uses curiously recurring template pattern.
 * \tparam LabelEnum The underlying enumeration (<tt>enum class</tt>)
 * \tparam ValueType The enumerator value type
 */
template<
    typename EnhancedEnum, typename LabelEnum, typename ValueType>
struct enum_base {
    static_assert( std::is_enum_v<LabelEnum> );

    using label_type = LabelEnum;   ///< \brief Alias for the label enum type
    using value_type = ValueType;   ///< \brief Alias for the value type

    /** \brief Return the size of the enumeration
     */
    static constexpr std::size_t size() noexcept
    {
        return EnhancedEnum::values.size();
    }

    /** \brief Return the signed size of the enumeration
     */
    static constexpr std::ptrdiff_t ssize() noexcept
    {
        return static_cast<std::ptrdiff_t>(size());
    }

    /** \brief Return iterator to the first enumerator
     *
     * \return A random access iterator to the beginning of the range
     * containing all enumerators in the order they are declared in
     * the enum
     */
    static constexpr auto begin() noexcept
    {
        return details::enum_iterator {
            EnhancedEnum {static_cast<LabelEnum>(0)}};
    }

    /** \brief Return iterator to one past the last enumerator
     *
     * \return Iterator to the end of the range pointed to by begin()
     */
    static constexpr auto end() noexcept
    {
        return details::enum_iterator {
            EnhancedEnum {static_cast<LabelEnum>(size())}};
    }

    /** \brief Return range over all enumerators
     *
     * \return A range containing all enumerators in the order they
     * are declared in the enum
     */
    static constexpr auto all() noexcept
    {
        return details::enum_range {begin(), end()};
    }

    /** \brief Return the enumerator with the given value
     *
     * \note The number of comparisons is linear in the size of the
     * enumeration. The assumption is that the number of enumerators
     * is small and the values are localized in memory, making linear
     * algorithm efficient in practice.
     *
     * \param value The value to search
     *
     * \return The first enumerator whose value is \p value, or empty
     * if no such enumerator exists
     */
    static constexpr std::optional<EnhancedEnum> from(const value_type& value) noexcept
    {
        for (const auto e : all()) {
            if (e.value() == value) {
                return e;
            }
        }
        return std::nullopt;
    }

    /** \brief Default constructor
     *
     * Construct an enumerator with indeterminate value
     */
    enum_base() = default;

    /** \brief Copy construct an enumerator
     *
     * Postcondition: <tt>this->get() == other.get()</tt>
     *
     * \param other The source enumerator
     */
    constexpr enum_base(const enum_base& other) noexcept = default;

    /** \brief Construct an enumerator with the given label
     *
     * Postcondition: <tt>this->get() == label</tt>.
     *
     * \param label The label enumerator
     */
    constexpr enum_base(const label_type& label) noexcept : label {label} {}

    /** \brief Copy assign an enumerator
     *
     * Postcondition: <tt>this->get() == other.get()</tt>
     *
     * \param other The source enumerator
     *
     * \return \c *this
     */
    constexpr enum_base& operator=(const enum_base& other) noexcept = default;

    /** \brief Return the label enumerator
     */
    constexpr label_type get() const noexcept
    {
        return label;
    }

    /** \brief Convert the enumerator to its underlying label enumerator
     *
     * \return <tt>this->get()</tt>
     */
    explicit constexpr operator label_type() const noexcept
    {
        return get();
    }

    /** \brief Return the value of the enumerator
     *
     * \throw std::out_of_range if \c *this is not a valid enumerator
     */
    constexpr const value_type& value() const noexcept
    {
        const auto n = static_cast<std::size_t>(label);
        return EnhancedEnum::values.at(n);
    }

private:
    LabelEnum label;
};

////////////////////////////////////////////////////////////////////////////////
// Template support
////////////////////////////////////////////////////////////////////////////////

/** \defgroup templatesupport Template support
 *
 * Support for writing templates with label enumerations and enhanced
 * enumerations.
 *
 * \{
 */

/** \brief Convert a label enumeration to an enhanced enumeration
 *
 * \tparam LabelEnum A label enum type (<tt>enum class</tt>)
 */
template<typename LabelEnum>
using enhanced = decltype(enhance(std::declval<LabelEnum>()));

/** \brief Check if a type in an enhanced enumeration
 *
 * If \c T is a type that derives from \ref enum_base, then \c
 * is_enhanced_enum derives from \c std::true_type. Otherwise derives
 * from \c std::false_type.
 *
 * \tparam T The type to check
 */
template<
    typename T
#ifndef IS_DOXYGEN
    , typename = void
#endif
>
struct is_enhanced_enum
#ifndef IS_DOXYGEN
    : std::false_type
#endif
{};

#ifndef IS_DOXYGEN

template<typename T>
struct is_enhanced_enum<
    T,
    std::enable_if_t<
        std::is_base_of_v<
            enum_base<T, typename T::label_type, typename T::value_type>,
            T
        >
    >
> : std::true_type {};

#endif

/** \brief Shorthand for \ref is_enhanced_enum
 */
template<typename T>
inline constexpr bool is_enhanced_enum_v = is_enhanced_enum<T>::value;

/** \brief Check if a type in a label enumeration
 *
 * If \c T is a type that has an associated enhanced enum type (see
 * \ref enhanced), the \c is_label_enum derives from \c
 * std::true_type. Otherwise derives from \c std::false_type.
 *
 * \tparam T The type to check
 */
template<
    typename T
#ifndef IS_DOXYGEN
    , typename = void
#endif
>
struct is_label_enum
#ifndef IS_DOXYGEN
    : std::false_type
#endif
{};

#ifndef IS_DOXYGEN

template<typename T>
struct is_label_enum<T, std::void_t<enhanced<T>>> : std::true_type {};

#endif

/** \brief Shorthand for \ref is_label_enum
 */
template<typename T>
inline constexpr bool is_label_enum_v = is_label_enum<T>::value;

/** \brief Makes an enumeration enhanced
 *
 * If \c Enum is either an enhanced enum (see \ref is_enhanced_enum)
 * or a label enum (see \ref is_label_enum), has the associated
 * enhanced enum as member typedef \c type. Otherwise has no member
 * typedefs.
 */
template<
    typename Enum
#ifndef IS_DOXYGEN
    , typename = void
#endif
>
struct make_enhanced;

#ifndef IS_DOXYGEN

template<typename Enum>
struct make_enhanced<Enum, std::enable_if_t<is_enhanced_enum_v<Enum>>>
{
    using type = Enum;
};

template<typename Enum>
struct make_enhanced<Enum, std::enable_if_t<is_label_enum_v<Enum>>>
{
    using type = enhanced<Enum>;
};

#endif

/** \brief Shorthand for \ref make_enhanced
 */
template<typename Enum>
using make_enhanced_t = typename make_enhanced<Enum>::type;

/** \brief Check if two types are the same once enhanced
 *
 * If \c T and \c U are either label enums or enhanced enums, and the
 * associated enhanced enum types are the same, derives from \c
 * std::true_type. Otherwise derives from \c std::false_type.
 *
 * This template is useful for writing generic comparison functions
 * that accepts both label and enhanced enums of the same kind.
 *
 * \code
 * template<
 *     typename Enum1, typename Enum2,
 *     typename = std::enable_if_t<is_same_when_enhanced_v<Enum1, Enum2>>
 * >
 * bool compare(Enum1 e1, Enum2 e2)
 * {
 *     // implementation can use ensure_enum(e1) to access the enhanced capabilities
 * }
 * \endcode
 */
template<
    typename T, typename U
#ifndef IS_DOXYGEN
    , typename = void
#endif
>
struct is_same_when_enhanced
#ifndef IS_DOXYGEN
    : std::false_type
#endif
{};

#ifndef IS_DOXYGEN

template<typename T, typename U>
struct is_same_when_enhanced<
    T, U,
    std::enable_if_t<
        std::is_same_v<make_enhanced_t<T>, make_enhanced_t<U>>
    >
> : std::true_type {};

#endif

/** \brief Shorthand for \ref is_same_when_enhanced
 */
template<typename T, typename U>
inline constexpr bool is_same_when_enhanced_v = is_same_when_enhanced<T, U>::value;

/** \brief Return enhanced enumerator associated with the argument
 *
 * \param e The enumerator to promote
 *
 * \return If \c Enum is a label enumeration, promote \p e to the
 * associated enhanced enumerator. If \c Enum is an enhanced
 * enumeration, return \p e as is.
 *
 * \sa is_same_when_enhanced for an example how this might be used in generic
 * code
 */
template<typename Enum>
constexpr make_enhanced_t<Enum> ensure_enhanced(Enum e) noexcept
{
    return static_cast<make_enhanced_t<Enum>>(e);
}

/// \}

////////////////////////////////////////////////////////////////////////////////
// Comparison operators
////////////////////////////////////////////////////////////////////////////////

#ifndef IS_DOXYGEN

template<
    typename Enum1, typename Enum2,
    typename = std::enable_if_t<is_same_when_enhanced_v<Enum1, Enum2>>
>
constexpr bool operator==(Enum1 lhs, Enum2 rhs) noexcept
{
    return ensure_enhanced(lhs).get() == ensure_enhanced(rhs).get();
}

template<
    typename Enum1, typename Enum2,
    typename = std::enable_if_t<is_same_when_enhanced_v<Enum1, Enum2>>
>
constexpr bool operator!=(Enum1 lhs, Enum2 rhs) noexcept
{
    return !(lhs == rhs);
}

template<
    typename Enum1, typename Enum2,
    typename = std::enable_if_t<is_same_when_enhanced_v<Enum1, Enum2>>
>
constexpr bool operator<(Enum1 lhs, Enum2 rhs) noexcept
{
    return ensure_enhanced(lhs).get() < ensure_enhanced(rhs).get();
}

template<
    typename Enum1, typename Enum2,
    typename = std::enable_if_t<is_same_when_enhanced_v<Enum1, Enum2>>
>
constexpr bool operator<=(Enum1 lhs, Enum2 rhs) noexcept
{
    return !(rhs < lhs);
}

template<
    typename Enum1, typename Enum2,
    typename = std::enable_if_t<is_same_when_enhanced_v<Enum1, Enum2>>
>
constexpr bool operator>(Enum1 lhs, Enum2 rhs) noexcept
{
    return rhs < lhs;
}

template<
    typename Enum1, typename Enum2,
    typename = std::enable_if_t<is_same_when_enhanced_v<Enum1, Enum2>>
>
constexpr bool operator>=(Enum1 lhs, Enum2 rhs) noexcept
{
    return !(lhs < rhs);
}

#endif // IS_DOXYGEN

/// \}

/** \brief Hash for enhanced enums
 *
 * This is a struct template satisfying the requirements of Hash for
 * enhanced enum types. Instantiating the template is possibly if and
 * only if <tt>\ref is_enhanced_enum_v<Enum> == true</tt>.
 *
 * \note Due to restrictions of the C++ standard library, the enhanced
 * enum library doesn't specialize the \c std::hash template. Please
 * see the user guide if you need a specialization of \c std::hash for
 * your own type.
 */
template<
    typename Enum
#ifndef IS_DOXYGEN
    , typename = std::enable_if_t<is_enhanced_enum_v<Enum>>
#endif
>
struct hash
{
    /** \brief Calculate hash for \p e
     */
    std::size_t operator()(const Enum& e) const noexcept
    {
        return std::hash<typename Enum::label_type>{}(e.get());
    }
};

}

#endif // ENHANCED_ENUM_HH_INCLUDED_
