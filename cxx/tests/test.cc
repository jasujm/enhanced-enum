#include <algorithm>
#include <array>
#include <ostream>

#include <gtest/gtest.h>

#include "status.hh"

using testapp::StatusLabel;
using testapp::EnhancedStatus;
namespace Statuses = testapp::Statuses;

namespace {

// Explicitly bundling label enum, enhanced enum and value to be consumed in the
// tests. Also defining operator<< to make the test reports pretty.

struct EnumBundle {
    StatusLabel label;
    EnhancedStatus enhanced;
    std::string_view value;
};

std::ostream& operator<<(std::ostream& os, const EnumBundle& bundle)
{
    return os << bundle.value;
}

}

// Compiling the test executable is already a test:

static_assert( std::is_trivial_v<EnhancedStatus> );
static_assert( std::is_standard_layout_v<EnhancedStatus> );
static_assert( std::is_same_v<EnhancedStatus::label_type, StatusLabel> );
static_assert( std::is_same_v<EnhancedStatus::value_type, std::string_view> );
static_assert( std::is_same_v<enhanced_enum::enhanced<StatusLabel>, EnhancedStatus> );
static_assert( enhanced_enum::is_enhanced_enum_v<EnhancedStatus> );
static_assert( !enhanced_enum::is_enhanced_enum_v<StatusLabel> );
static_assert( !enhanced_enum::is_label_enum_v<EnhancedStatus> );
static_assert( enhanced_enum::is_label_enum_v<StatusLabel> );
static_assert( std::is_same_v<enhanced_enum::make_enhanced_t<StatusLabel>, EnhancedStatus> );
static_assert( std::is_same_v<enhanced_enum::make_enhanced_t<EnhancedStatus>, EnhancedStatus> );

// Basic functions

static_assert( EnhancedStatus::size() == 3u );
static_assert( EnhancedStatus::ssize() == 3 );
static_assert( enhance(StatusLabel::BUSY).get() == StatusLabel::BUSY );
static_assert( enhance(StatusLabel::BUSY).value() == Statuses::BUSY_VALUE );
static_assert( EnhancedStatus::from(Statuses::BUSY_VALUE) == Statuses::BUSY );
static_assert( !EnhancedStatus::from("nonexistent") );

// Comparison operators work as expected, and can compare both enhanced and
// label enums

static_assert( enhance(StatusLabel::BUSY) == StatusLabel::BUSY );
static_assert( StatusLabel::BUSY == enhance(StatusLabel::BUSY) );

static_assert( enhance(StatusLabel::BUSY) != StatusLabel::INITIALIZING );
static_assert( StatusLabel::BUSY != enhance(StatusLabel::INITIALIZING) );

static_assert( enhance(StatusLabel::INITIALIZING) < StatusLabel::BUSY );
static_assert( StatusLabel::INITIALIZING < enhance(StatusLabel::BUSY) );

static_assert( enhance(StatusLabel::INITIALIZING) <= StatusLabel::BUSY );
static_assert( StatusLabel::INITIALIZING <= enhance(StatusLabel::BUSY) );
static_assert( enhance(StatusLabel::BUSY) <= StatusLabel::BUSY );
static_assert( StatusLabel::BUSY <= enhance(StatusLabel::BUSY) );

static_assert( enhance(StatusLabel::BUSY) > StatusLabel::INITIALIZING );
static_assert( StatusLabel::BUSY > enhance(StatusLabel::INITIALIZING) );

static_assert( enhance(StatusLabel::BUSY) >= StatusLabel::INITIALIZING );
static_assert( StatusLabel::BUSY >= enhance(StatusLabel::INITIALIZING) );
static_assert( enhance(StatusLabel::BUSY) >= StatusLabel::BUSY );
static_assert( StatusLabel::BUSY >= enhance(StatusLabel::BUSY) );

// Iterators

static_assert( std::distance(EnhancedStatus::begin(), EnhancedStatus::end()) == 3 );
static_assert( std::distance(EnhancedStatus::end(), EnhancedStatus::begin()) == -3 );
static_assert( EnhancedStatus::all().size() == 3u );
static_assert( EnhancedStatus::begin() == EnhancedStatus::begin()++ );
static_assert( EnhancedStatus::begin() != ++EnhancedStatus::begin() );
static_assert( EnhancedStatus::begin() < EnhancedStatus::end() );
static_assert( EnhancedStatus::begin() + 3 == EnhancedStatus::end() );
static_assert( EnhancedStatus::end() - 3 == EnhancedStatus::begin() );
static_assert( *EnhancedStatus::begin() == Statuses::INITIALIZING );
static_assert( EnhancedStatus::begin()->value() == Statuses::INITIALIZING_VALUE );
static_assert( *++EnhancedStatus::begin() == Statuses::WAITING_FOR_INPUT );
static_assert( EnhancedStatus::begin()[1] == Statuses::WAITING_FOR_INPUT );
static_assert( *(EnhancedStatus::begin() + 2) == Statuses::BUSY );
static_assert( *--EnhancedStatus::end() == Statuses::BUSY );
static_assert( *(EnhancedStatus::end() - 2) == Statuses::WAITING_FOR_INPUT );

// Test nested enum type

static_assert(
    std::is_same_v<
       nested::NestedEnum::value_type,
       std::tuple<long, std::tuple<std::string_view, bool>>
    >
);

static_assert(
    nested::NestedEnums::enumerator_value ==
    std::tuple { 0, std::tuple { "string", true } }
);

// Non-compile time tests start here:

class EnhancedEnumTest : public testing::TestWithParam<EnumBundle> {};

// Construction

TEST_P(EnhancedEnumTest, testGetLabelEnum)
{
    const auto bundle = GetParam();
    EXPECT_EQ(bundle.enhanced.get(), bundle.label);
}

TEST_P(EnhancedEnumTest, testValue)
{
    const auto bundle = GetParam();
    EXPECT_EQ(bundle.enhanced.value(), bundle.value);
}

TEST_P(EnhancedEnumTest, testConstructFromValue)
{
    const auto bundle = GetParam();
    EXPECT_EQ(EnhancedStatus::from(bundle.value), bundle.enhanced);
}

// Ranges and iterators

TEST_F(EnhancedEnumTest, testAll)
{
    const auto all_enumerators = EnhancedStatus::all();
    EXPECT_TRUE(
        std::equal(
            all_enumerators.begin(), all_enumerators.end(),
            EnhancedStatus::begin(), EnhancedStatus::end()));
}

TEST_F(EnhancedEnumTest, testIterator)
{
    auto iter = EnhancedStatus::begin();
    EXPECT_EQ(*iter++, Statuses::INITIALIZING);
    EXPECT_EQ(*iter++, Statuses::WAITING_FOR_INPUT);
    EXPECT_EQ(*iter++, Statuses::BUSY);
    EXPECT_EQ(iter, EnhancedStatus::end());
}

TEST_F(EnhancedEnumTest, testIteratorReversal)
{
    auto iter = EnhancedStatus::end();
    EXPECT_EQ(*--iter, Statuses::BUSY);
    EXPECT_EQ(*--iter, Statuses::WAITING_FOR_INPUT);
    EXPECT_EQ(*--iter, Statuses::INITIALIZING);
    EXPECT_EQ(iter, EnhancedStatus::begin());
}

TEST_F(EnhancedEnumTest, testIteratorRandomAccess)
{
    const auto iter = EnhancedStatus::begin();
    EXPECT_EQ(iter[0], Statuses::INITIALIZING);
    EXPECT_EQ(iter[1], Statuses::WAITING_FOR_INPUT);
    EXPECT_EQ(iter[2], Statuses::BUSY);
}

TEST_F(EnhancedEnumTest, testIteratorRandomAccessReversal)
{
    const auto iter = EnhancedStatus::end();
    EXPECT_EQ(iter[-3], Statuses::INITIALIZING);
    EXPECT_EQ(iter[-2], Statuses::WAITING_FOR_INPUT);
    EXPECT_EQ(iter[-1], Statuses::BUSY);
}

INSTANTIATE_TEST_SUITE_P(
    WithEnumBundle,
    EnhancedEnumTest,
    testing::Values(
        EnumBundle {
            StatusLabel::INITIALIZING,
            Statuses::INITIALIZING,
            Statuses::INITIALIZING_VALUE,
        },
        EnumBundle {
            StatusLabel::WAITING_FOR_INPUT,
            Statuses::WAITING_FOR_INPUT,
            Statuses::WAITING_FOR_INPUT_VALUE,
        },
        EnumBundle {
            StatusLabel::BUSY,
            Statuses::BUSY,
            Statuses::BUSY_VALUE,
        }
    )
);
