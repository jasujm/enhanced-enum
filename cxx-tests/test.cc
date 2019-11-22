#include <gtest/gtest.h>

#include "status.hh"

using namespace testapp;

static_assert( std::is_trivial_v<EnhancedStatus> );
static_assert( std::is_standard_layout_v<EnhancedStatus> );
static_assert( std::is_same_v<EnhancedStatus::label_type, StatusLabel> );
static_assert( std::is_same_v<EnhancedStatus::value_type, std::string_view> );
static_assert( enhance(StatusLabel::BUSY).get() == StatusLabel::BUSY );
static_assert( enhance(StatusLabel::INITIALIZING).value() == StatusDetails::INITIALIZING_VALUE );

TEST(EnhancedEnumTest, stub)
{
    EXPECT_TRUE(true);
}
